from django.db import models
from django.db.models.deletion import CASCADE, PROTECT

TIPO_CONTA = (
    ('RE', 'RECEITA'),
    ('DE', 'DESPESA'),
    ('IN', 'INVESTIMENTO')
)

BANCO_CHOICES = (
    ('BP', 'BANRISUL PASQUALOTO'),
    ('BRP', 'BANRISUL RP'),
    ('SP', 'SICREDI')
)

class Conta(models.Model):
    cod = models.CharField(max_length=6)
    conta = models.CharField(max_length=80)
    tipo = models.CharField(max_length=2, choices=TIPO_CONTA, null=True, blank=True)

    def __str__(self):
        return self.conta

class Pessoa(models.Model):
    desc = models.CharField(max_length=40)


class CC(models.Model):
    data = models.DateField()
    desc = models.CharField(max_length=80)
    banco = models.CharField(max_length=4, choices=BANCO_CHOICES, null=True, blank=True)
    conta = models.ForeignKey(Conta, on_delete=PROTECT, null=True, blank=True)
    pessoa = models.ForeignKey(Pessoa, on_delete=PROTECT, null=True, blank=True)
    credito = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    debito = models.DecimalField(max_digits=13, decimal_places=2, default=0)

    def __str__(self):
        return self.desc