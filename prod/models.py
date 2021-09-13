from django.db import models
from django.db.models.deletion import PROTECT
from django.urls import reverse_lazy


class Unid(models.Model):
    unid = models.CharField("Unidade", max_length=3)
    desc = models.CharField("Descrição", max_length=30)

    def __str__(self):
        return self.unid

class Grupo(models.Model):
    cod = models.CharField("Código", max_length=15)
    desc = models.CharField("Descrição", max_length=40)
    cod_cyber = models.IntegerField()

    def __str__(self):
        return self.desc

class NCM(models.Model):
    cod = models.CharField("NCM", max_length=8)
    desc = models.CharField("Descrição", max_length=40)

    def __str__(self):
        return self.cod
#Produto
class Prod(models.Model):
    cod = models.CharField("Código", max_length=15)
    desc = models.CharField("Descrição", max_length=50)
    compl = models.CharField("Complemento",
                             max_length=50,
                             blank=True,
                             null=True)
    grupo = models.ForeignKey(Grupo, on_delete = PROTECT)
    unid = models.ForeignKey(Unid, on_delete = PROTECT)
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
    cmv = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        verbose_name="CMV",
        blank=True, null=True
        )
    qEst = models.DecimalField(
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
        on_delete = PROTECT
        )
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

    def __str__(self):
        return self.desc

class ProdComp(models.Model):
    codProd = models.ForeignKey(
        Prod,
        related_name='codProd',
        verbose_name="CodProd",
        on_delete = PROTECT
        )
    codComp = models.ForeignKey(
        Prod,
        related_name='codComp',
        verbose_name="CodComp",
        on_delete = PROTECT
        )
    qtd = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        verbose_name="Quantidade"
        )

#Obsoleto
class Produto(models.Model):
    importado = models.BooleanField(default=False)
    ncm = models.CharField('NCM', max_length=8)
    produto = models.CharField(max_length=100, unique=True)
    preco = models.DecimalField('preço', max_digits=7, decimal_places=2)
    estoque = models.IntegerField('estoque atual')
    estoque_minimo = models.PositiveIntegerField('estoque mínimo', default=0)
    data = models.DateField(null=True, blank=True)
    categoria = models.ForeignKey(
        'Categoria',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('produto',)

    def __str__(self):
        return self.produto

    def get_absolute_url(self):
        return reverse_lazy('produto:produto_detail', kwargs={'pk': self.pk})

    def to_dict_json(self):
        return {
            'pk': self.pk,
            'produto': self.produto,
            'estoque': self.estoque,
        }


class Categoria(models.Model):
    categoria = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('categoria',)

    def __str__(self):
        return self.categoria
