from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from datetime import datetime    


class Unid(models.Model):
    unid = models.CharField("Unidade", max_length=3)
    desc = models.CharField("Descrição", max_length=30, blank=True, null=True)

    def __str__(self):
        return self.unid

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
    cod = models.CharField("Tipo de Produto", max_length=4)
    desc = models.CharField("Descrição", max_length=40)

    def __str__(self):
        return self.cod + ' - ' + self.desc

class Grupo(models.Model):
    cod = models.CharField("Código", max_length=4)
    desc = models.CharField("Descrição", max_length=40)
    cod_cyber = models.IntegerField()

    def __str__(self):
        return self.desc

class SubGrupo(models.Model):
    cod = models.CharField("Código", max_length=4)
    desc = models.CharField("Descrição", max_length=40)
    cod_cyber = models.IntegerField()

    def __str__(self):
        return self.desc

#Produto
class Prod(models.Model):
    cod = models.CharField("Código", max_length=20, unique=True)
    desc = models.CharField("Descrição", max_length=50)
    compl = models.CharField("Complemento",
                             max_length=50,
                             blank=True,
                             null=True)
    tipoProduto = models.ForeignKey(TipoProduto, on_delete = PROTECT, blank=True, null=True)
    grupo = models.ForeignKey(Grupo, on_delete = PROTECT, blank=True, null=True)
    subGrupo = models.ForeignKey(SubGrupo, on_delete = PROTECT, blank=True, null=True)
    grupoCyber = models.IntegerField(blank=True, null=True)
    unid = models.ForeignKey(Unid, related_name='unid1', on_delete = PROTECT)
    unid2 = models.ForeignKey(Unid, related_name='unid2',on_delete = PROTECT, blank=True, null=True)
    fatorUnid = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=1,
        verbose_name="Fator de conversão",
        blank=True, null=True
        )
    unidCyber = models.CharField(max_length=4, blank=True, null=True)
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
    origemFiscal = models.ForeignKey(OrigemFiscal, on_delete = PROTECT, default=1, blank=True, null=True)
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
        default='0',
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

class ProdComp(models.Model):
    codProd = models.ForeignKey(
        Prod,
        related_name='codigoProd',
        verbose_name='CodProd',
        on_delete = CASCADE
        )
    codComp = models.ForeignKey(
        Prod,
        related_name='codigoComp',
        verbose_name="CodComp",
        on_delete = CASCADE
        )
    qtd = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        verbose_name="Quantidade"
        )
    criado = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    criadoPor = models.ForeignKey(User, related_name='prodcomp_criou', on_delete=models.CASCADE, blank=True, null=True)
    modificado = models.DateTimeField(auto_now=True, blank=True, null=True)
    modificadoPor = models.ForeignKey(User, related_name='prodcomp_modificou', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
            return str(self.codProd.pk) + ' - ' + str(self.codComp.desc)
        
    def get_comp_name(self):
        return self.codComp.desc
