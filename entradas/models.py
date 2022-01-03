from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from comercial.models import STATUS_OPCOES, Entrega, Vencimento
from cadastro.models import Parceiro
from financeiro.models import Plano_contas
from prod.models import Prod

class Operacao_entrada(models.Model):
    desc = models.CharField(max_length=30)
    conta_credito = models.ForeignKey(Plano_contas, on_delete=PROTECT, related_name='entrada_op_credito')
    conta_debito = models.ForeignKey(Plano_contas, on_delete=PROTECT, related_name='entrada_op_debito')

class NF_entrada(models.Model):
    num = models.IntegerField(default=0)
    data_emissao = models.DateField()
    parceiro = models.ForeignKey(Parceiro, on_delete=PROTECT, related_name='entradas')
    transportadora = models.ForeignKey(Parceiro, on_delete=PROTECT, related_name='fretes_entradas')
    operacao = models.ForeignKey(Operacao_entrada, on_delete=PROTECT)
    vencimento = models.ForeignKey(Vencimento, on_delete=PROTECT)
    valor_total_produtos = models.DecimalField(max_digits=13, decimal_places=2)
    valor_frete = models.DecimalField(max_digits=13, decimal_places=2)
    valor_outras_desp = models.DecimalField(max_digits=13, decimal_places=2)
    valor_total_nota = models.DecimalField(max_digits=13, decimal_places=2)

class NF_entrada_itens(models.Model):
    nf_entrada = models.ForeignKey(NF_entrada, on_delete=CASCADE)
    produto = models.ForeignKey(Prod, on_delete=PROTECT)
    qtd = models.DecimalField(max_digits=13, decimal_places=4)
    preco_unit = models.DecimalField(max_digits=13, decimal_places=4)
    preco_tot = models.DecimalField(max_digits=13, decimal_places=2)
    aliq_icms = models.DecimalField(max_digits=5, decimal_places=1)
    aliq_ipi = models.DecimalField(max_digits=5, decimal_places=1)
    valor_ipi = models.DecimalField(max_digits=13, decimal_places=2)

class Ordem_compra(models.Model):
    num = models.IntegerField(default=0)
    data_emissao = models.DateField()
    data_previsao = models.DateField()
    prazo_entrega = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_OPCOES)
    parceiro = models.ForeignKey(Parceiro, on_delete=PROTECT, related_name='ordem_compra')
    transportadora = models.ForeignKey(Parceiro, on_delete=PROTECT, related_name='fretes_oc')
    operacao = models.ForeignKey(Operacao_entrada, on_delete=PROTECT)
    vencimento = models.ForeignKey(Vencimento, on_delete=PROTECT)
    valor_total_produtos = models.DecimalField(max_digits=13, decimal_places=2)
    valor_frete = models.DecimalField(max_digits=13, decimal_places=2)
    valor_outras_desp = models.DecimalField(max_digits=13, decimal_places=2)
    valor_total_nota = models.DecimalField(max_digits=13, decimal_places=2)

class Ordem_compra_itens(models.Model):
    ordem_compra = models.ForeignKey(Ordem_compra, on_delete=CASCADE)
    produto = models.ForeignKey(Prod, on_delete=PROTECT)
    qtd = models.DecimalField(max_digits=13, decimal_places=4)
    preco_unit = models.DecimalField(max_digits=13, decimal_places=4)
    preco_tot = models.DecimalField(max_digits=13, decimal_places=2)
    aliq_icms = models.DecimalField(max_digits=5, decimal_places=1)
    aliq_ipi = models.DecimalField(max_digits=5, decimal_places=1)
    valor_ipi = models.DecimalField(max_digits=13, decimal_places=2)
    obs = models.CharField(max_length=40, null=True, blank=True)

class Solicitacao_material(models.Model):
    num = models.IntegerField(default=0)
    data_emissao = models.DateField()
    data_previsao = models.DateField()
    prazo_entrega = models.PositiveSmallIntegerField()
    valor_total = models.DecimalField(max_digits=13, decimal_places=2)

class Solicitacao_material_item(models.Model):
    solicitacao_material = models.ForeignKey(Solicitacao_material, on_delete=CASCADE)
    produto = models.ForeignKey(Prod, on_delete=PROTECT)
    qtd = models.DecimalField(max_digits=13, decimal_places=4)
    preco_unit = models.DecimalField(max_digits=13, decimal_places=4)
    valor_tot = models.DecimalField(max_digits=13, decimal_places=2)
    aliq_icms = models.DecimalField(max_digits=5, decimal_places=1)
    aliq_ipi = models.DecimalField(max_digits=5, decimal_places=1)
    valor_ipi = models.DecimalField(max_digits=13, decimal_places=2)
    valor_tot_ipi = models.DecimalField(max_digits=13, decimal_places=2)
    obs = models.CharField(max_length=40, null=True, blank=True)