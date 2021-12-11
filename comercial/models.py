from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models import F
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from datetime import datetime    
from prod.models import Prod
from cadastro.models import Parceiro


class Vencimento(models.Model):
    vencimentos = models.CharField("Vencimentos", max_length=30, default='0')

    def __str__(self):
        return self.vencimentos

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


class Operacao(models.Model):
    desc = models.CharField("Nome", max_length=30, null=True, blank=True)
    desc_NF = models.CharField("Desc. na NF", max_length=30, null=True, blank=True)
    CFOP = models.CharField("Nome", max_length=5, null=True, blank=True)
    CSOSN = models.CharField("CSOSN", max_length=5, choices=CSOSN_OPCOES, null=True, blank=True)
    Origem_mercadoria = models.CharField("CSOSN", max_length=5, choices=ORIGEM_OPCOES, null=True, blank=True)
    mensagem_NF = models.TextField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.desc

STATUS_OPCOES = (
    (0,'ORÇAMENTO'),
    (10,'PEDIDO NOVO'),
    (20,'PEDIDO PROGRAMADO'),
    (30,'PEDIDO PRONTO PARA FATURAMENTO'),
    (40,'PEDIDO FATURADO AGUARDANDO EXPEDIÇÃO'),
    (50,'PEDIDO ENTREGUE E ENCERRADO'),
)

class PedidoManager(models.Manager):
    """QuerySet manager for Invoice class to add non-database fields.

    A @property in the model cannot be used because QuerySets (eg. return
    value from .all()) are directly tied to the database Fields -
    this does not include @property attributes."""

    def get_queryset(self):
        """Overrides the models.Manager method"""
        qs = super(PedidoManager, self).get_queryset().annotate(saldo = F('valor_total_pedido') - F('valor_total_entregue'))
        return qs


class Pedido(models.Model):
    num = models.CharField("Número", max_length=15, default='0', unique=True)
    operacao = models.ForeignKey(Operacao, on_delete = PROTECT, null=True, blank=True)
    status = models.PositiveIntegerField(choices=STATUS_OPCOES, default=0)
    data_cadastro = models.DateTimeField(blank=True, null=True)
    data_previsao = models.DateTimeField(blank=True, null=True)
    cliente = models.ForeignKey(Parceiro, related_name='pedidos', on_delete = PROTECT, null=True, blank=True)
    vencimentos = models.ForeignKey(Vencimento, on_delete = PROTECT, related_name='pedidos', null=True, blank=True)
    transportadora = models.ForeignKey(Parceiro, related_name='pedidos_tranportados', on_delete = PROTECT, null=True, blank=True)
    tipo_frete = models.CharField(max_length=1, choices=TIPO_FRETE, default='1')
    obs = models.TextField(blank=True, null=True)
    valor_total_pedido = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_total_entregue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_total_saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    objects = PedidoManager()

    @property
    def valor_saldo(self):
        return self.valor_total_pedido - self.valor_total_entregue


    def __str__(self):
        return self.num
        


class Pedido_item(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=CASCADE)
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
    saldo = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
        verbose_name="Saldo",
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
    obs = models.CharField(max_length=50, blank=True, null=True)

    @property
    def pr_tot(self):
        return self.qtd * self.pr_unit


    def __str__(self):
        return self.produto.desc    



'''

class NCM(models.Model):
    cod = models.CharField("NCM", max_length=12)
    desc = models.CharField("Descrição", max_length=40)

    def __str__(self):
        return self.cod

class OrigemFiscal(models.Model):
    cod = models.CharField("Origem Fiscal", max_length=12)
    desc = models.CharField("Descrição", max_length=40)

    def __str__(self):
        return self.cod

class TipoProduto(models.Model):
    cod = models.CharField("Tipo de Produto", max_length=12)
    desc = models.CharField("Descrição", max_length=40)

    def __str__(self):
        return self.cod

#Produto
class Prod(models.Model):
    cod = models.CharField("Código", max_length=15, unique=True)
    desc = models.CharField("Descrição", max_length=50)
    compl = models.CharField("Complemento",
                             max_length=50,
                             blank=True,
                             null=True)
    grupo = models.ForeignKey(Grupo, on_delete = CASCADE)
    grupoCyber = models.IntegerField(blank=True, null=True)
    unid = models.ForeignKey(Unid, related_name='unid1', on_delete = CASCADE)
    unid2 = models.ForeignKey(Unid, related_name='unid2',on_delete = CASCADE, blank=True, null=True)
    fatorUnid = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=1,
        verbose_name="Fator de conversão",
        blank=True, null=True
        )
    unidCyber = models.CharField(max_length=4, blank=True, null=True)
    tipoProduto = models.ForeignKey(TipoProduto, on_delete = CASCADE, blank=True, null=True)
    pLiq = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        verbose_name="Peso Líquido",
        blank=True, null=True
        )
    pBrt = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        verbose_name="Peso Bruto",
        blank=True, null=True
        )
    prAq = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        verbose_name="Preço Aquisição",
        blank=True, null=True
        )
    prVenda = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        verbose_name="Preço Venda",
        blank=True, null=True
        )
    prCusto = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        verbose_name="Preço Custo",
        blank=True, null=True
        )
    cmv = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        verbose_name="CMV",
        blank=True, null=True
        )
    qEstoque = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        verbose_name="Estoque",
        blank=True, null=True
        )
    qEstMin = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        verbose_name="Estoque Mínimo",
        blank=True, null=True
        )
    qEstMax = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        verbose_name="Estoque Máximo",
        blank=True, null=True
        )
    qMult = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        verbose_name="Qtd. Múltipla de compra",
        blank=True, null=True
        )
    qEco = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        verbose_name="Qtd. Econômica",
        blank=True, null=True
        )
    pzEnt = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        verbose_name="Prazo Entrega",
        blank=True, null=True
        )
    #Impostos
    origemFiscal = models.ForeignKey(OrigemFiscal, on_delete = CASCADE, blank=True, null=True)
    ipiCompra = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name="IPI Compra",
        blank=True, null=True
        )
    ipiVenda = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name="IPI Compra",
        blank=True, null=True
        )
    icmsCompra = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name="ICMS Compra",
        blank=True, null=True
        )
    icmsVenda = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name="ICMS Venda",
        blank=True, null=True)
    ncm =  models.ForeignKey(
        NCM,
        verbose_name="NCM",
        blank=True, null=True,
        on_delete = CASCADE
        )
    NCMCyber = models.CharField(max_length=11, blank=True, null=True)
    origFiscal = models.CharField(
        "Origem Fiscal",
        max_length=2,
        blank=True, null=True
        )
    tipoTributacao = models.CharField(
        "Tipo de Tributação",
        max_length=2,
        blank=True, null=True
        )
    obs = models.TextField(blank=True, null=True)

    criado = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    criadoPor = models.ForeignKey(User, related_name='prod_criou', on_delete=models.CASCADE, blank=True, null=True)
    modificado = models.DateTimeField(auto_now=True, blank=True, null=True)
    modificadoPor = models.ForeignKey(User, related_name='prod_modificou', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.cod + ' - ' + self.desc 
'''