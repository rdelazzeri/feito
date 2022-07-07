from pydoc import describe
from decimal import Decimal
from datetime import datetime, timedelta
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from comercial.models import Entrega
from cadastro.models import Parceiro
from entradas.models import NF_entrada
#from entradas.models import NF_entrada

TIPO_CHOICES = (
    ('CR', 'CONTAS A RECEBER'),
    ('CP', 'CONTAS A PAGAR'),
)


class Vencimento_Manager(models.Manager):
    def parcelas_create(self, vencimento, valor_total, data_emissao ):
        #v = Vencimento.objects.get(id = venc_id)
        print(vencimento)
        vc = str(vencimento.vencimentos)
        parcelas = vc.split(sep = ' + ')
        print(parcelas)
        num_parc = len(parcelas)
        print(num_parc)
        val_tot = Decimal(valor_total)
        val_parc = round((val_tot / num_parc),2)
        val_parc_saldo = (val_tot - num_parc * val_parc)
        val_parc_1 = val_parc_saldo + val_parc
        print('Valor total fatura: ' + str(val_tot) + 'Valor do saldo: ' + str(val_parc_saldo) + 'Valor parcela: ' + str(val_parc) + 'Valor Parcela 1: ' + str(val_parc_1))
        parc = []
        print(parc)
        for n, parcela in enumerate(parcelas):
            print(parcela)
            p = {}   
            p['numero'] = n + 1
            p['vencimento'] = data_emissao + timedelta(days=int(parcela))
            p['valor_parcela'] = val_parc_1 if n == 0 else val_parc
            print(p)
            parc.append(p)
        return parc


class Vencimento(models.Model):
    vencimentos = models.CharField("Vencimentos", max_length=30, default='0')
    objects = Vencimento_Manager()

    def __str__(self):
        return str(self.vencimentos)


class Plano_contas(models.Model):
    num = models.IntegerField()
    desc = models.CharField(max_length=50)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, null=True, blank=True)
    cod_cyber = models.CharField(max_length=12, null=True, blank=True)
    banco = models.CharField(max_length=1, null=True, blank=True)
    nivel = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return str(self.desc)

class Status(models.Model):
    desc = models.CharField(max_length=30)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)

    def __str__(self) -> str:
        return self.desc

class Banco(models.Model):
    nome = models.CharField(max_length=40)
    codigo = models.CharField(max_length=4, null=True, blank=True)
    agencia = models.CharField(max_length=6, null=True, blank=True)
    conta = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        return self.nome

class Origem(models.Model):
    desc = models.CharField(max_length=20)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)

    def __str__(self):
        return self.desc

class Conta_receber(models.Model):
    entrega = models.ForeignKey(Entrega, on_delete=CASCADE, null=True, blank=True, related_name='parcelas')
    parceiro = models.ForeignKey('cadastro.Parceiro', on_delete=CASCADE, null=True, blank=True, related_name='contas_receber')
    nf_num = models.IntegerField(default=0)
    parcela_num = models.IntegerField(default=0)
    data_emissao = models.DateField(null=True, blank=True)
    data_vencimento = models.DateField(null=True, blank=True)
    valor_parcela = models.DecimalField(decimal_places=2, max_digits=13, default=0)
    conta_caixa = models.ForeignKey(Plano_contas, on_delete=PROTECT, null=True, blank=True)
    data_pagamento = models.DateField(null=True, blank=True)
    valor_pago = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    status = models.ForeignKey(Status, on_delete=PROTECT, null=True, blank=True)
    banco = models.ForeignKey(Banco, on_delete=PROTECT, null=True, blank=True)
    origem = models.ForeignKey(Origem, on_delete=PROTECT, null=True, blank=True)
    obs = models.TextField(null=True, blank=True)
    
    class Meta: 
        verbose_name = "Conta a Receber"
        verbose_name_plural = "Contas a Receber"
    
    def __str__(self):
        return 'num.: ' + str(self.parcela_num) + ' val: ' + str(self.valor_parcela)


class Conta_pagar_manager(models.Manager):
    def parcelas_add(nf_id):
        nf = NF_entrada.objects.get(id=nf_id)
        

class Conta_pagar(models.Model):
    entrada = models.ForeignKey('entradas.NF_entrada', on_delete=CASCADE, null=True, blank=True, related_name='parcelas')
    parceiro = models.ForeignKey('cadastro.Parceiro', on_delete=CASCADE, null=True, blank=True, related_name='contas_pagar')
    num_nf = models.IntegerField(default=0)
    num_parcela = models.IntegerField(default=0)
    data_emissao = models.DateField(null=True, blank=True)
    data_vencimento = models.DateField(null=True, blank=True)
    valor_parcela = models.DecimalField(decimal_places=2, max_digits=13, default=0)
    conta_caixa = models.ForeignKey(Plano_contas, on_delete=PROTECT, null=True, blank=True)
    data_pagamento = models.DateField(null=True, blank=True)
    valor_pago = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    status = models.ForeignKey(Status, on_delete=PROTECT, null=True, blank=True)
    banco = models.ForeignKey(Banco, on_delete=PROTECT, null=True, blank=True)
    origem = models.ForeignKey(Origem, on_delete=PROTECT, null=True, blank=True)
    obs = models.TextField(null=True, blank=True)
    
    def __str__(self):
        #return 'num.: ' + str(self.parcela_num) + ' val: ' + str(self.valor_parcela)
        return str(self.id)
    

class Diario(models.Model):
    data = models.DateField()
    desc = models.CharField(max_length=40)
    parceiro = models.ForeignKey(Parceiro, on_delete=PROTECT)
    conta = models.ForeignKey(Plano_contas, on_delete=PROTECT)
    credito = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    debito = models.DecimalField(max_digits=13, decimal_places=2, default=0)

    def __str__(self):
        return self.desc
        

class CC(models.Model):
    data = models.DateField()
    desc = models.CharField(max_length=40)
    parceiro = models.ForeignKey(Parceiro, on_delete=PROTECT)
    credito = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    debito = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    saldo = models.DecimalField(max_digits=13, decimal_places=2, default=0)

    def __str__(self):
        return self.desc


