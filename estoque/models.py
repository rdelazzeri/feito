from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from comercial.models import Entrega
from cadastro.models import Parceiro
from prod.models import Prod

class Estoque_movimento(models.Model):
    data = models.DateField()
    desc = models.CharField(max_length=40)
    produto = models.ForeignKey(Prod, on_delete=PROTECT)
    proprietario = models.ForeignKey(Parceiro, on_delete=PROTECT)
    quantidade = models.DecimalField(max_digits=13, decimal_places=3, default=0)
    valor = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    