from django.db import models 
from django.apps import apps
from django.apps import AppConfig
#from django.db.models import get_model
from django.db.models.deletion import CASCADE, PROTECT
from comercial.models import STATUS_OPCOES
from cadastro.models import Parceiro
#from estoque.models import Movimento
#from financeiro.models import Plano_contas
from prod.models import Prod
from decimal import Decimal
from django.db.models import Sum

TIPO_FRETE = (
    ('1','CIF'),
    ('2','FOB'),
)

STATUS_OC_OPCOES = (
    ('1','COTAÇÃO DE PREÇOS'),
    ('2','ORDEM DE COMPRA'),
)

class Operacao_entrada(models.Model):
    desc = models.CharField(max_length=30)
    conta_credito = models.ForeignKey('financeiro.Plano_contas', on_delete=PROTECT, related_name='entrada_op_credito')
    conta_debito = models.ForeignKey('financeiro.Plano_contas', on_delete=PROTECT, related_name='entrada_op_debito')
    conta_caixa = models.ForeignKey('financeiro.Plano_contas', on_delete=PROTECT, related_name='entrada_conta_caixa')

    def __str__(self) -> str:
        return str(self.desc)

class NF_entrada(models.Model):
    num = models.IntegerField(default=0)
    serie = models.CharField(max_length=5, null=True, blank=True)
    num_oc = models.IntegerField(default=0)
    data_emissao = models.DateField()
    parceiro = models.ForeignKey(Parceiro, on_delete=PROTECT, related_name='entradas')
    transportadora = models.ForeignKey(Parceiro, on_delete=PROTECT, related_name='fretes_entradas', null=True, blank=True)
    tipo_frete = models.CharField(max_length=1, choices=TIPO_FRETE, default='2', null=True, blank=True)
    operacao = models.ForeignKey(Operacao_entrada, on_delete=PROTECT, null=True, blank=True)
    conta = models.ForeignKey('financeiro.Plano_contas', on_delete=PROTECT, null=True, blank=True)
    vencimento = models.ForeignKey('financeiro.Vencimento', on_delete=PROTECT, null=True, blank=True)
    valor_total_produtos = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    valor_frete = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    valor_outras_desp = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    base_calc_icms = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    valor_icms = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    base_calc_icms_st = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    valor_icms_st = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    valor_seguro = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    desconto = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    valor_ipi = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    valor_total_nota = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    chave_cyber = models.CharField(max_length=15, null=True, blank=True)
    serie_cyber = models.CharField(max_length=4, null=True, blank=True)

    
    def calcula_total(self):
        itens = (NF_entrada_itens.objects.filter(nf_entrada_id = self.id)
            .aggregate(
                SUM_PRODUTOS = Sum('preco_tot'),
                SUM_ICMS = Sum('valor_icms'),
                SUM_IPI = Sum('valor_ipi')
                )
            )
        
        f = True if itens['SUM_PRODUTOS'] else False               
        self.valor_total_produtos = itens['SUM_PRODUTOS'] if f else 0
        self.base_calc_icms = self.valor_total_produtos if f else 0
        self.valor_icms = itens['SUM_ICMS'] if f else 0
        self.valor_ipi = itens['SUM_IPI'] if f else 0
        self.save()
       
    def delete(self, *args, **kwargs):
        for item in self.itens.all():
            item.delete()
        super().delete()
    
    def save(self, *args, **kwargs):
        vtp = Decimal(self.valor_total_produtos)
        vf = Decimal(self.valor_frete)
        vod = Decimal(self.valor_outras_desp)
        icms = Decimal(self.valor_icms)
        seg = Decimal(self.valor_seguro)
        ipi = Decimal(self. valor_ipi)
        desc = Decimal(self. desconto)
        self.valor_total_nota = vtp + vf + vod + seg + ipi - desc
        super().save()


    def __str__(self) -> str:
        num = "{:<20}".format(self.num)
        return 'NF: ' + num + str(self.parceiro)

class NF_entrada_itens(models.Model):
    nf_entrada = models.ForeignKey(NF_entrada, on_delete=CASCADE, related_name='itens')
    produto = models.ForeignKey(Prod, on_delete=PROTECT)
    cfop = models.CharField(max_length=5, blank=True, null=True)
    qtd = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    preco_unit = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    preco_tot = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    aliq_icms = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    aliq_ipi = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    valor_icms = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    valor_ipi = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    valor_total_item = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    obs = models.CharField(max_length=100, null=True, blank=True)
    
    def delete(self, *args, **kwargs):
        tipo = 'NF_E'
        pk = self.id
        m = apps.get_model('estoque.Movimento')
        m.objects.movimento_delete(tipo, pk)
        super().delete()
        self.nf_entrada.calcula_total()
    
    def save(self, *args, **kwargs):
        if self.qtd is None: self.qtd = 0
        if self.preco_unit is None: self.preco_unit = 0
        if Decimal(self.qtd) > 0:
            self.preco_tot = Decimal(self.qtd) * Decimal(self.preco_unit)
            self.valor_icms = Decimal(self.preco_tot) * Decimal(self.aliq_icms) * Decimal(0.01)
            self.valor_ipi = Decimal(self.preco_tot) * Decimal(self.aliq_ipi) * Decimal(0.01)
            self.valor_total_item = Decimal(self.preco_tot) + Decimal(self.valor_ipi)
            
            parc = self.nf_entrada.parceiro.apelido
            num = self.nf_entrada.num

            mov = {}
            mov['data'] = self.nf_entrada.data_emissao
            mov['desc'] = 'NF Entrada de: %s núm.: %s' %(parc, num)
            mov['produto'] = self.produto
            mov['qtd_entrada'] = self.qtd
            mov['qtd_saida'] = 0
            mov['valor'] = self.preco_unit
            mov['tipo'] = 'NF_E'
            mov['chave'] = num
             
            m = apps.get_model('estoque.Movimento')
            m.objects.movimento_save(mov)
        super().save()
        self.nf_entrada.calcula_total()

    def __str__(self) -> str:
        #prod = "{:<20}".format(self.produto.cod)
        return str(self.produto.cod)

class Ordem_compra(models.Model):
    num = models.IntegerField(default=0)
    data_emissao = models.DateField()
    data_previsao = models.DateField()
    prazo_entrega = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_OC_OPCOES)
    parceiro = models.ForeignKey(Parceiro, on_delete=PROTECT, related_name='ordem_compra')
    transportadora = models.ForeignKey(Parceiro, on_delete=PROTECT, related_name='fretes_oc')
    operacao = models.ForeignKey(Operacao_entrada, on_delete=CASCADE)
    vencimento = models.ForeignKey('financeiro.Vencimento', on_delete=PROTECT)
    valor_total_produtos = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    valor_frete = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    valor_outras_desp = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    base_calc_icms = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    valor_icms = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    base_calc_icms_st = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    valor_icms_st = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    valor_seguro = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    desconto = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    valor_ipi = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    valor_total_oc = models.DecimalField(max_digits=13, decimal_places=2, default=0)


    def calcula_total(self):
        itens = (Ordem_compra_itens.objects.filter(ordem_compra_id = self.id)
            .aggregate(
                SUM_PRODUTOS = Sum('preco_tot'),
                SUM_ICMS = Sum('valor_icms'),
                SUM_IPI = Sum('valor_ipi')
                )
            )
        
        f = True if itens['SUM_PRODUTOS'] else False               
        self.valor_total_produtos = itens['SUM_PRODUTOS'] if f else 0
        self.valor_icms = itens['SUM_ICMS'] if f else 0
        self.valor_ipi = itens['SUM_IPI'] if f else 0
        self.save()

    def save(self, *args, **kwargs):
        vtp = Decimal(self.valor_total_produtos)
        vf = Decimal(self.valor_frete)
        vod = Decimal(self.valor_outras_desp)
        #icms = Decimal(self.valor_icms)
        seg = Decimal(self.valor_seguro)
        ipi = Decimal(self. valor_ipi)
        desc = Decimal(self. desconto)
        self.valor_total_oc = vtp + vf + vod + seg + ipi - desc
        super().save()

class Ordem_compra_itens(models.Model):
    ordem_compra = models.ForeignKey(Ordem_compra, on_delete=CASCADE, related_name='itens')
    produto = models.ForeignKey(Prod, on_delete=PROTECT)
    qtd = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    preco_unit = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    preco_tot = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    aliq_icms = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    aliq_ipi = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    valor_icms = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    valor_ipi = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    obs = models.CharField(max_length=40, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.qtd is None: self.qtd = 0
        if self.preco_unit is None: self.preco_unit = 0
        if Decimal(self.qtd) > 0:
            self.preco_tot = Decimal(self.qtd) * Decimal(self.preco_unit)
            #self.aliq_icms = Decimal(self.preco_tot) * Decimal(self.aliq_icms) * Decimal(0.01)
            #self.aliq_ipi = Decimal(self.preco_tot) * Decimal(self.aliq_ipi) * Decimal(0.01)
            #self.preco_tot = Decimal(self.preco_tot) + Decimal(self.valor_ipi)
            self.valor_ipi = Decimal(self.preco_tot) * Decimal(self.aliq_ipi) * Decimal(0.01)
            self.valor_icms = Decimal(self.preco_tot) * Decimal(self.aliq_icms) * Decimal(0.01)

        super().save()
        self.ordem_compra.calcula_total()

    def delete(self, *args, **kwargs):
        super().delete()
        self.ordem_compra.calcula_total()


class Solicitacao_material(models.Model):
    num = models.IntegerField(default=0)
    data_emissao = models.DateField()
    data_previsao = models.DateField()
    prazo_entrega = models.PositiveSmallIntegerField()
    valor_total = models.DecimalField(max_digits=13, decimal_places=2, default=0)

class Solicitacao_material_item(models.Model):
    solicitacao_material = models.ForeignKey(Solicitacao_material, on_delete=CASCADE)
    produto = models.ForeignKey(Prod, on_delete=PROTECT)
    qtd = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    preco_unit = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    valor_tot = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    aliq_icms = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    aliq_ipi = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    valor_ipi = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    valor_tot_ipi = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    obs = models.CharField(max_length=40, null=True, blank=True)