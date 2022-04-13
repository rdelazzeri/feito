from django.db import models
from django.db.models.deletion import PROTECT
from django.utils import timezone
from django.contrib.auth.models import User
from django_cpf_cnpj.fields import CPFField, CNPJField
#from localflavor.br.models import *

class Tipo_parceiro(models.Model):
    desc = models.CharField(max_length=20)
    sigla = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return self.desc

class Estado(models.Model):
    cod = models.IntegerField()
    sigla = models.CharField(primary_key=True, max_length=2)
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.sigla


class Municipio(models.Model):
    cod = models.CharField(primary_key=True, max_length=7)
    nome = models.CharField(max_length=35)
    estado = models.ForeignKey(Estado, on_delete = models.CASCADE)

    def __str__(self):
        return self.nome


class Parceiro(models.Model):
    tipo = models.ManyToManyField(Tipo_parceiro,  blank=True, related_name='tipo')
    pessoa_choices = (('F', 'Física'), ('J', 'Jurídica'))
    pessoa = models.CharField(max_length=2, choices=pessoa_choices, default='J',)
    nome = models.CharField(max_length=120, verbose_name='Nome',  blank=True, null=True)
    apelido = models.CharField(max_length=60, blank=True, null=True)
    data_cadastro = models.DateField(blank=True, null=True)
    #docs pj
    cnpj =CNPJField(masked=True,  blank=True, null=True)
    #cnpj2 = BRCNPJField(null=True)
    insc_est = models.CharField(max_length=31,  blank=True, null=True)
    insc_mun = models.CharField(max_length=31,  blank=True, null=True)
    #docs PF
    cpf = CPFField(masked=True,  blank=True, null=True)
    #cpf2 = BRCPFField(null=True)
    #endereco
    logradouro = models.CharField(max_length=60,blank=True, null=True)
    numero = models.CharField(max_length=15,blank=True, null=True)
    complemento = models.CharField(max_length=60, blank=True, null=True)
    bairro = models.CharField(max_length=60, blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True)
    #estado = models.ForeignKey(Estado, blank=True, null=True, on_delete = models.PROTECT)
    estado = models.CharField(max_length=2, blank=True, null=True)
    cidade = models.CharField(max_length=60, null=True, blank=True)
    municipio = models.ForeignKey(Municipio, blank=True, null=True, on_delete = models.PROTECT)
    #Contato
    fone1 = models.CharField(max_length=15, blank=True, null=True)
    fone2 = models.CharField(max_length=15, blank=True, null=True)
    email_nfe = models.CharField(max_length=500, blank=True, null=True)
    email_contato = models.CharField(max_length=500, blank=True, null=True)
    #Obs
    obs = models.TextField(max_length=5000, blank=True, null=True)
    suframa = models.CharField(max_length=15, blank=True, null=True)
    cod_cyber = models.CharField(max_length=15, blank=True, null=True)
    

    def __str__(self):
        return str(self.nome)

class Tipo_end(models.Model):
    tipo_end = models.CharField(max_length=40)
    
    def __str__(self):
        return self.tipo_end

class Endereco(models.Model):
    #Endereco
    tipo_end = models.ForeignKey(Tipo_end, on_delete=models.PROTECT)
    desc_end = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=60,blank=True, null=True)
    numero = models.CharField(max_length=15,blank=True, null=True)
    complemento = models.CharField(max_length=30, blank=True, null=True)
    bairro = models.CharField(max_length=30, blank=True, null=True)
    cep = models.CharField(max_length=8, blank=True, null=True)
    estado = models.ForeignKey(Estado, blank=True, null=True, on_delete = models.PROTECT)
    municipio = models.ForeignKey(Municipio, blank=True, null=True, on_delete = models.PROTECT)

    def __str__(self):
        return self.desc_end


class Empresa(models.Model):

    razsoc = models.CharField(max_length=120, verbose_name='Nome',  blank=True, null=True)
    fantasia = models.CharField(max_length=60, blank=True, null=True)
    data_cadastro = models.DateField(blank=True, null=True)
    #docs pj
    cnpj =CNPJField(masked=True,  blank=True, null=True)
    #cnpj2 = BRCNPJField(null=True)
    insc_est = models.CharField(max_length=31,  blank=True, null=True)
    insc_mun = models.CharField(max_length=31,  blank=True, null=True)
    #docs PF
    #endereco
    logradouro = models.CharField(max_length=60,blank=True, null=True)
    numero = models.CharField(max_length=15,blank=True, null=True)
    complemento = models.CharField(max_length=60, blank=True, null=True)
    bairro = models.CharField(max_length=60, blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True)
    #estado = models.ForeignKey(Estado, blank=True, null=True, on_delete = models.PROTECT)
    estado = models.CharField(max_length=2, blank=True, null=True)
    cidade = models.CharField(max_length=60, null=True, blank=True)
    municipio = models.ForeignKey(Municipio, blank=True, null=True, on_delete = models.PROTECT)
    #Contato
    fone1 = models.CharField(max_length=15, blank=True, null=True)
    fone2 = models.CharField(max_length=15, blank=True, null=True)
    email_nfe = models.CharField(max_length=500, blank=True, null=True)
    email_contato = models.CharField(max_length=500, blank=True, null=True)
    #Obs
    obs = models.TextField(max_length=5000, blank=True, null=True)
    suframa = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return str(self.razsoc)