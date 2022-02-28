from decimal import Decimal
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models import F
from django.db.models.enums import Choices
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from datetime import datetime, timedelta
#from financeiro.models import Plano_contas   
from prod.models import Prod
from cadastro.models import Parceiro
from django.db.models import Avg, Count, Min, Sum
import datetime

class Comercial_config(models.Model):
    num_ult_orcamento = models.PositiveIntegerField("Número último orçamento", default='0')
    num_ult_pedido = models.PositiveIntegerField("Número último pedido", default='0')
    num_ult_entrega = models.PositiveIntegerField("Número última entrega", default='0')
    num_ult_nf = models.PositiveIntegerField("Número última NF", default='0')

    def __str__(self):
        return 'Configurações comerciais'




TIPO_FRETE = (
    ('1','CIF'),
    ('2','FOB'),
)

TIPO_PEDIDO = (
    ('1','ORÇAMENTO'),
    ('2','PEDIDO'),
)

TIPO_SITUACAO = (
    ('1','ATIVO'),
    ('2','ENCERRADO'),
)

CSOSN_OPCOES = (
    ('101','TRIBUTADO'),
    ('102','...'),
)

ORIGEM_OPCOES = (
    ('0','NACIONAL'),
    ('1','ESTRANGEIRA'),
)

OPERACAO_MOVIMENTO = (
    ('0','ENTRADA'),
    ('1','SAÍDA'),
)

FINALIDADE_OPCOES = (
    ('1','NF-e normal'),
    ('4','DevoluçãoA'),
)

SITUACAO_TRIBUTARIA_OPCOES = (
    ('101', 'Tributada com permissão de crédito'),
    ('102', 'Tributada sem permissão de crédito'),
    ('103', 'Isenção do ICMS para faixa de receita bruta'),
    ('201', 'Tributada com permissão de crédito e com cobrança do ICMS por substituição tributária'),
    ('202', 'Tributada sem permissão de crédito e com cobrança do ICMS por substituição tributária'),
    ('203', 'Isenção do ICMS para faixa de receita bruta e com cobrança do ICMS por substituição tributária'),
    ('300', 'Imune'),
    ('400', 'Não tributada'),
    ('500', 'ICMS cobrado anteriormente por substituição tributária (substituído) ou por antecipação'),
    ('900', 'Outros'),
)


class Operacao(models.Model):
    desc = models.CharField("Nome", max_length=30, null=True, blank=True)
    natureza_operacao = models.CharField("Desc. na NF", max_length=60, null=True, blank=True)
    tipo = models.CharField('Movimento', default=1, max_length=1, choices=OPERACAO_MOVIMENTO)
    CFOP = models.CharField("Nome", max_length=5, null=True, blank=True)
    CSOSN = models.CharField("CSOSN", max_length=5, choices=CSOSN_OPCOES, null=True, blank=True)
    situacao_tributaria = models.CharField('Sit. Trib.', max_length=3, choices=SITUACAO_TRIBUTARIA_OPCOES)
    origem_mercadoria = models.CharField("CSOSN", max_length=1, choices=ORIGEM_OPCOES, null=True, blank=True)
    finalidade = models.CharField("Finalidade", max_length=1, choices=FINALIDADE_OPCOES, null=True, blank=True)
    mensagem_NF = models.TextField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    classe_imposto = models.CharField("Classe do imposto", max_length=15, null=True, blank=True)
    conta_caixa = models.ForeignKey('financeiro.Plano_contas', on_delete=PROTECT, null=True, blank=True)

    def __str__(self):
        return str(self.desc)

STATUS_OPCOES = (
    (0,'ORÇAMENTO'),
    (10,'PEDIDO NOVO'),
    (20,'PEDIDO PROGRAMADO'),
    (30,'PEDIDO PRONTO PARA FATURAMENTO'),
    (40,'PEDIDO FATURADO AGUARDANDO EXPEDIÇÃO'),
    (50,'PEDIDO ENTREGUE E ENCERRADO'),
)

ORCAMENTO_OPCOES = (
    (0,'PENDENTE'),
    (10,'PEDIDO NOVO'),
    (20,'PEDIDO PROGRAMADO'),
    (30,'PEDIDO PRONTO PARA FATURAMENTO'),
    (40,'PEDIDO FATURADO AGUARDANDO EXPEDIÇÃO'),
    (50,'PEDIDO ENTREGUE E ENCERRADO'),
)

class Orcamento_status(models.Model):
    desc = models.CharField("Nome", max_length=30, null=True, blank=True)

    def __str__(self):
        return str(self.desc)

class Orcamento_origem(models.Model):
    desc = models.CharField("Nome", max_length=30, null=True, blank=True)

    def __str__(self):
        return str(self.desc)


class Orcamento(models.Model):
    num_orc = models.PositiveIntegerField("Número Orçamento", default=0, null=True, blank=True)
    num_orc_cli = models.CharField("Número Cliente", max_length=15,  null=True, blank=True)
    status = models.ForeignKey(Orcamento_status, on_delete=PROTECT, null=True, blank=True)
    origem = models.ForeignKey(Orcamento_origem, on_delete=PROTECT, null=True, blank=True)
    operacao = models.ForeignKey(Operacao, on_delete = PROTECT, null=True, blank=True)
    cliente = models.ForeignKey(Parceiro, related_name='orcamentos', on_delete = PROTECT, null=True, blank=True)
    data_cadastro = models.DateTimeField(blank=True, null=True)
    data_previsao = models.DateTimeField(blank=True, null=True)
    previsao_entrega = models.PositiveSmallIntegerField('Prazo de entrega', default=0, blank=True, null=True)
    validade_orcamento = models.PositiveSmallIntegerField('Validade orcamento', default=7, blank=True, null=True)
    vencimentos = models.ForeignKey('financeiro.Vencimento', on_delete = PROTECT, related_name='orcamentos', null=True, blank=True)
    transportadora = models.ForeignKey(Parceiro, related_name='orcamentos_transportados', on_delete = PROTECT, null=True, blank=True)
    tipo_frete = models.CharField(max_length=1, choices=TIPO_FRETE, default='2')
    valor_frete = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    obs = models.TextField(max_length=5000,  blank=True, null=True)
    valor_total_produtos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_total_orcamento = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    #def __str__(self):
    #    return 'Número: '

def calcula_total_orcamento(orcamento):
    orc_tot = Orcamento_item.objects.filter(orcamento_id = orcamento).aggregate(TOTAL = Sum('pr_tot'))['TOTAL']
    orc = Orcamento.objects.get(pk = orcamento)
    orc.valor_total_produtos = orc_tot
    orc.valor_total_orcamento = orc_tot + orc.valor_frete
    orc.save()



class Orcamento_item(models.Model):
    orcamento = models.ForeignKey(Orcamento, on_delete=CASCADE, related_name='itens')
    produto = models.ForeignKey(Prod, on_delete=PROTECT, null=True, blank=True)
    qtd = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Qtd",
        )
    pr_unit = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Preço Unit.",
        )
    pr_tot = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Preço Total.",
        )
    aliq_ICMS = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Aliq ICMS",
        )
    aliq_IPI = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Aliq IPI",
        )
    val_ICMS = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Valor ICMS",
        )
    val_IPI = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Valor IPI",
        )
    obs = models.CharField(max_length=500, blank=True, null=True)

    #def __str__(self):
    #    return self.produto.desc 

    def save(self):
        t = float(self.qtd) * float(self.pr_unit)
        self.pr_tot =  t
        super().save()
        calcula_total_orcamento(self.orcamento.pk)


    def delete(self):
        super().delete()
        calcula_total_orcamento(self.orcamento.pk)


class PedidoManager(models.Manager):
    """QuerySet manager for Invoice class to add non-database fields.

    A @property in the model cannot be used because QuerySets (eg. return
    value from .all()) are directly tied to the database Fields -
    this does not include @property attributes."""

    def get_queryset(self):
        """Overrides the models.Manager method"""
        qs = super(PedidoManager, self).get_queryset().annotate(saldo = F('valor_total_pedido') - F('valor_total_entregue'))
        return qs





def calcula_total_pedido(pedido_id):
    ped_tot = Pedido_item.objects.filter(pedido_id = pedido_id).aggregate(TOTAL = Sum('pr_tot'))['TOTAL']
    ped = Pedido.objects.get(pk = pedido_id)
    ped.valor_total_pedido = ped_tot
    ped.valor_total_saldo = ped_tot - ped.valor_total_entregue
    ped.save()
   

class Pedido(models.Model):
    num = models.PositiveIntegerField(default='0', unique=True)
    operacao = models.ForeignKey(Operacao, on_delete = PROTECT, null=True, blank=True)
    status = models.PositiveIntegerField(choices=STATUS_OPCOES, default=0)
    data_cadastro = models.DateTimeField(blank=True, null=True)
    data_previsao = models.DateTimeField(blank=True, null=True)
    cliente = models.ForeignKey(Parceiro, related_name='pedidos', on_delete = PROTECT, null=True, blank=True)
    vencimentos = models.ForeignKey('financeiro.Vencimento', on_delete = PROTECT, related_name='pedidos', null=True, blank=True)
    transportadora = models.ForeignKey(Parceiro, related_name='pedidos_tranportados', on_delete = PROTECT, null=True, blank=True)
    tipo_frete = models.CharField(max_length=1, choices=TIPO_FRETE, default='1')
    valor_frete = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    obs = models.TextField(max_length=5000,  blank=True, null=True)
    obs_nf = models.TextField(max_length=5000,blank=True, null=True)
    valor_total_pedido = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_total_entregue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_total_saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    #objects = PedidoManager()

    
    def __str__(self):
        return str(self.num)
        
class Pedido_item(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=CASCADE, related_name='itens')
    produto = models.ForeignKey(Prod, on_delete=PROTECT, null=True, blank=True)
    qtd = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Qtd",
        )
    pr_unit = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Preço Unit.",
        )
    pr_tot = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Preço Total.",
        )
    qtd_entregue = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Qtd Entregue",
        )
    val_entregue = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Valor faturado",
        )
    qtd_saldo = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Saldo Qtd",
        )
    valor_saldo = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Saldo R$",
        )

    aliq_ICMS = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Aliq ICMS",
        )
    aliq_IPI = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Aliq IPI",
        )
    val_ICMS = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Valor ICMS",
        )
    val_IPI = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Valor IPI",
        )
    codigo_cfop = models.CharField('CFOP', max_length=4)
    obs = models.CharField(max_length=50, blank=True, null=True)
    inf_adic = models.CharField(max_length=500, blank=True, null=True)

    def save(self):
        t = Decimal(self.qtd) * Decimal(self.pr_unit)
        self.pr_tot =  t
        self.valor_saldo = Decimal(self.pr_tot) - Decimal(self.val_entregue)
        self.qtd_saldo = Decimal(self.qtd) - Decimal(self.qtd_entregue)
        super().save()
        calcula_total_pedido(self.pedido.pk)


    def __str__(self):
        return self.produto.desc    


ENTREGA_OPCOES = (
    (0,'RASCUNHO'),
    (1,'ERRO NA TRANSMISSÃO'),
    (2,'EMITIDA'),
)

'''
def entrega_parcela_add(entrega, valor_total, vencimentos):
    parcelas = str(vencimentos.vencimentos).split(sep = '+')
    num_parc = len(parcelas)
    val_tot = Decimal(valor_total)
    val_parc = round((val_tot / num_parc),2)
    val_parc_saldo = (val_tot - num_parc * val_parc)
    val_parc_1 = val_parc_saldo + val_parc
    print('Valor total fatura: ' + str(val_tot) + 'VAlor do saldo: ' + str(val_parc_saldo) + 'Valor parcela: ' + str(val_parc) + 'Valor Parcela 1: ' + str(val_parc_1))
    hoje = datetime.date.today()
    n=0
    for parcela in parcelas:
        n +=1
        if n < 10:
            np = '0' + str(n)
        else:
            np = str(n)
        numparc = int(str(entrega.num_nf) + np)
        
        try:
            parc = Entrega_parcelas.objects.get(entrega = entrega, num = numparc)
        except:
            parc = Entrega_parcelas()
        
        parc.entrega = entrega
        parc.num = numparc
        parc.vencimento = datetime.date.today() + timedelta(days=int(parcela))
        if n == 1:
            parc.valor_parcela = val_parc_1
        else:
            parc.valor_parcela = val_parc
        parc.save()

    print('Vencimentos original: ' + vencimentos.vencimentos)
    print('Número de parcelas: ' + str(num_parc))
    print('hoje: ' + str(hoje))


def calcula_total_entrega(entrega_id):
    ent_tot = Entrega_item.objects.filter(entrega_id = entrega_id).aggregate(TOTAL = Sum('pr_tot'))['TOTAL']
    ent = Entrega.objects.get(pk = entrega_id)
    ent.valor_total_produtos = ent_tot
    ent.valor_total_entrega = ent_tot + ent.valor_frete
    ent.save()
    entrega_parcela_add(ent, ent.valor_total_entrega, ent.vencimentos)

'''

class Entrega(models.Model):
    num = models.PositiveIntegerField("Número", default='0', unique=True)
    num_nf = models.IntegerField("Número da NFe", default='0')
    status = models.PositiveIntegerField(choices=ENTREGA_OPCOES, default=0)
    operacao = models.ForeignKey(Operacao, on_delete = PROTECT, null=True, blank=True)
    cliente = models.ForeignKey(Parceiro, related_name='entregas', on_delete = PROTECT, null=True, blank=True)
    data_cadastro = models.DateTimeField(blank=True, null=True)
    data_emissao = models.DateTimeField(blank=True, null=True)
    pedido_origem = models.ForeignKey(Pedido, related_name='entregas', on_delete=CASCADE, null=True, blank=True)
    vencimentos = models.ForeignKey('financeiro.Vencimento', on_delete = PROTECT, related_name='entregas', null=True, blank=True)
    transportadora = models.ForeignKey(Parceiro, related_name='entregas_tranportadas', on_delete = PROTECT, null=True, blank=True)
    tipo_frete = models.CharField(max_length=1, choices=TIPO_FRETE, default='1')
    valor_frete = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    volumes = models.CharField(max_length=15, null=True, blank=True)
    peso_bruto = models.CharField(max_length=15, null=True, blank=True)
    peso_liquido = models.CharField(max_length=15, null=True, blank=True)
    marca = models.CharField(max_length=15, null=True, blank=True)
    obs = models.TextField(max_length=5000,  blank=True, null=True)
    obs_nf = models.TextField(max_length=5000,blank=True, null=True)
    valor_total_produtos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_total_entrega = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def update_total(self):
        ent_tot = Entrega_item.objects.filter(entrega = self).aggregate(TOTAL = Sum('pr_tot'))['TOTAL']
        self.valor_total_produtos = ent_tot
        self.valor_total_entrega = ent_tot + self.valor_frete
        hoje = datetime.date.today()
        self.data_emissao = hoje
        self.save()

        parcelas = str(self.vencimentos).split(sep = '+')
        num_parc = len(parcelas)
        val_tot = Decimal(self.valor_total_entrega)
        val_parc = round((val_tot / num_parc),2)
        val_parc_saldo = (val_tot - num_parc * val_parc)
        val_parc_1 = val_parc_saldo + val_parc
        print('Valor total fatura: ' + str(val_tot) + 'Valor do saldo: ' + str(val_parc_saldo) + 'Valor parcela: ' + str(val_parc) + 'Valor Parcela 1: ' + str(val_parc_1))
        
        
        entrega_parcelas = Entrega_parcelas.objects.filter(entrega = self).delete()
        print('Parcelas deletadas')
        '''
        n_parc = entrega_parcelas.count()
        print('numro de parcelas: ' + str(n_parc))
        dif_n_parc =  n_parc - num_parc
        if dif_n_parc > 0:
            for i in range(dif_n_parc):
                n = i + num_parc
                parc = entrega_parcelas[n] 
                parc.delete()
                print('parcelas extras deletadas')
        '''
                
        for n, parcela in enumerate(parcelas):
            parc = Entrega_parcelas()   
            parc.entrega = self
            print('vencimento parcelas')
            parc.num = n + 1
            parc.vencimento = datetime.date.today() + timedelta(days=int(parcela))
            if n == 0:
                parc.valor_parcela = val_parc_1
            else:
                parc.valor_parcela = val_parc
            parc.save()

            print('Vencimentos original: ' + str(self.vencimentos))
            print('Número de parcelas: ' + str(num_parc))
            print('hoje: ' + str(hoje))

    

class Entrega_parcelas(models.Model):
    entrega = models.ForeignKey(Entrega, on_delete=CASCADE)
    num = models.CharField("Número", max_length=13)
    vencimento = models.DateTimeField()
    valor_parcela = models.DecimalField(max_digits=12, decimal_places=2, default=0)

 
class Entrega_item(models.Model):
    entrega = models.ForeignKey(Entrega, on_delete=CASCADE)
    produto = models.ForeignKey(Prod, on_delete=PROTECT, null=True, blank=True)
    pedido_item = models.ForeignKey(Pedido_item, on_delete=PROTECT, null=True, blank=True)
    oc_cliente = models.CharField("OC Cliente", max_length=13, null=True, blank=True)
    qtd = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Qtd",
        )
    pr_unit = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Preço Unit.",
        )
    pr_tot = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Preço Total.",
        )
    aliq_ICMS = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Aliq ICMS",
        )
    aliq_IPI = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Aliq IPI",
        )
    val_ICMS = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Valor ICMS",
        )
    val_IPI = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Valor IPI",
        )
    codigo_cfop = models.CharField('CFOP', max_length=4, blank=True, null=True)
    obs = models.CharField(max_length=50, blank=True, null=True)
    inf_adic = models.CharField(max_length=500, blank=True, null=True)


    def __str__(self):
        return self.produto.desc 

    def save(self):
        qtd = str(self.qtd)
        pr_unit = str(self.pr_unit)
        pr_tot = Decimal(qtd) * Decimal(pr_unit)
        t = round(pr_tot, 2)
        self.pr_tot =  t
        super().save()
        #calcula_total_entrega(self.entrega.pk)
        self.entrega.update_total()