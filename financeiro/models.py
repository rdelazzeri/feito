from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from comercial.models import Entrega
from cadastro.models import Parceiro

TIPO_CHOICES = (
    ('CR', 'CONTAS A RECEBER'),
    ('CP', 'CONTAS A PAGAR'),
)

class Plano_contas(models.Model):
    num = models.IntegerField()
    desc = models.CharField(max_length=50)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)

class Status(models.Model):
    desc = models.CharField(max_length=30)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)

class Banco(models.Model):
    nome = models.CharField(max_length=40)
    codigo = models.CharField(max_length=4, null=True, blank=True)
    agencia = models.CharField(max_length=6, null=True, blank=True)
    conta = models.CharField(max_length=20, null=True, blank=True)

class Origem(models.Model):
    desc = models.CharField(max_length=20)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)

class Conta_receber(models.Model):
    entrega = models.ForeignKey(Entrega, on_delete=CASCADE, null=True, blank=True)
    parcela_num = models.IntegerField(default=0)
    data_emissao = models.DateField()
    vencimento = models.DateField()
    valor_parcela = models.DecimalField(decimal_places=2, max_digits=13, default=0)
    conta_caixa = models.ForeignKey(Plano_contas, on_delete=PROTECT)
    data_pagamento = models.DateField()
    valor_pago = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    status = models.ForeignKey(Status, on_delete=PROTECT)
    banco = models.ForeignKey(Banco, on_delete=PROTECT)
    origem = models.ForeignKey(Origem, on_delete=PROTECT)

class Conta_pagar(models.Model):
    entrada = models.ForeignKey(Entrega, on_delete=CASCADE, null=True, blank=True)
    parcela_num = models.IntegerField(default=0)
    data_emissao = models.DateField()
    vencimento = models.DateField
    valor_parcela = models.DecimalField(decimal_places=2, max_digits=13, default=0)
    conta_caixa = models.ForeignKey(Plano_contas, on_delete=PROTECT)
    data_pagamento = models.DateField()
    valor_pago = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    status = models.ForeignKey(Status, on_delete=PROTECT)
    banco = models.ForeignKey(Banco, on_delete=PROTECT)
    origem = models.ForeignKey(Origem, on_delete=PROTECT)

class Diario(models.Model):
    data = models.DateField()
    desc = models.CharField(max_length=40)
    parceiro = models.ForeignKey(Parceiro, on_delete=PROTECT)
    conta = models.ForeignKey(Plano_contas, on_delete=PROTECT)
    credito = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    debito = models.DecimalField(max_digits=13, decimal_places=2, default=0)




