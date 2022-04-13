from unittest.mock import DEFAULT
from django.db import models 
from django.apps import apps
from django.db.models.deletion import CASCADE, PROTECT
from estoque.models import Movimento
from prod.models import ProdComp
from prod.models import Prod
from cadastro.models import Parceiro
from decimal import Decimal
from django.db.models import Sum

SETOR_PRODUTIVO = (
    ('1','CORTE'),
    ('2','FOB'),
)

UNIDADE_TEMPO = (
    ('1', 'MINUTO'),
    ('60', 'HORAS'),
    ('480', 'DIAS 8H')
)

STATUS_OP = (
    ('1', 'EMITIDA'),
    ('2', 'PLANEJADA'),
    ('3', 'PROGRAMADA'),
    ('4', 'EM PRODUÇÃO'),
    ('5', 'PRODUÇÃO PARCIAL'),
    ('6', 'CONCLUÍDA'),
    ('7', 'ENCERRADA COM SALDO'),
    ('8', 'CANCELADA')
)

class OP(models.Model):
    num = models.BigIntegerField(default=0)
    produto = models.ForeignKey('prod.Prod', on_delete=PROTECT, related_name='OPs')
    qtd_programada = models.DecimalField(max_digits=13, decimal_places=4, default=0, null=True, blank=True)
    data_emissao = models.DateField(null=True, blank=True)
    data_previsao = models.DateField(null=True, blank=True)
    data_encerramento = models.DateField(null=True, blank=True)
    tempo_estimado = models.DecimalField(default=0, max_digits=13, decimal_places=4, null=True, blank=True)
    momento_ini = models.DateTimeField(null=True, blank=True)
    momento_fim = models.DateTimeField(null=True, blank=True)
    tempo_realizado = models.DecimalField(null=True, blank=True, max_digits=13, decimal_places=4)
    qtd_realizada = models.DecimalField(default=0, null=True, blank=True, max_digits=13, decimal_places=4)
    qtd_perda = models.DecimalField(default=0, null=True, blank=True, max_digits=13, decimal_places=4)
    operador = models.ForeignKey('cadastro.Parceiro', on_delete=PROTECT, null=True, blank=True)
    setor_produtivo = models.CharField(max_length=2, choices=SETOR_PRODUTIVO, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_OP, default='1', null=True, blank=True)

    def save(self):
        super().save()
        comp_fis = ProdComp.objects.filter(codProd = self.produto)
        n = OP_componente_fisico.objects.filter(op = self).count()
        print('este é o n')
        print(n)
        if n == 0:
            for it in comp_fis:
                comp = OP_componente_fisico()
                comp.op = self
                comp.produto = it.codComp
                comp.qtd_programada = Decimal(self.qtd_programada) * Decimal(it.qtd)
                if comp.produto.cmv:
                    comp.custo_unitario = comp.produto.cmv
                    
                else:
                    comp.custo_unitario = 0
                comp.custo_total = Decimal(comp.custo_unitario) * Decimal(comp.qtd_programada)
                comp.save()
        else:
            print('passei')


    def __str__(self) -> str:
        return self.produto.desc


class OP_componente_fisico(models.Model):
    op = models.ForeignKey(OP, on_delete=CASCADE, related_name='op_comp_fis')
    produto = models.ForeignKey('prod.Prod', on_delete=PROTECT, related_name='comp_fis')
    qtd_programada = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    qtd_utilizada = models.DecimalField(default=0, max_digits=13, decimal_places=4, null=True, blank=True)
    nivel = models.IntegerField(default=0, null=True, blank=True)
    qtd_perda = models.DecimalField(default=0, null=True, blank=True, max_digits=13, decimal_places=4)
    custo_unitario = models.DecimalField(default=0, max_digits=13, decimal_places=4)
    custo_total = models.DecimalField(default=0, max_digits=13, decimal_places=4)

    def __str__(self) -> str:   
        return self.produto.desc

class OP_componente_servico_interno(models.Model):
    op = models.ForeignKey(OP, on_delete=CASCADE, related_name='op_serv_int')
    produto = models.ForeignKey('prod.Prod', on_delete=PROTECT, related_name='prod_serv_int')
    nivel = models.IntegerField(default=0)
    operador = models.ForeignKey('cadastro.Parceiro', on_delete=PROTECT, related_name='operador_serv_int', null=True, blank=True)
    unidade_tempo = models.CharField(choices = UNIDADE_TEMPO, default='1', max_length=6)
    tempo_estimado = models.DecimalField(default=0, max_digits=13, decimal_places=4)
    momento_ini = models.DateTimeField(null=True, blank=True)
    momento_fim = models.DateTimeField(null=True, blank=True)
    tempo_realizado = models.DecimalField(null=True, blank=True, max_digits=13, decimal_places=4)
    tempo_parada = models.IntegerField(default=0)
    custo_unitario = models.DecimalField(default=0, max_digits=13, decimal_places=4)
    custo_total = models.DecimalField(default=0, max_digits=13, decimal_places=4)


    def __str__(self) -> str:
        return self.produto.desc

class OP_componente_servico_externo(models.Model):
    op = models.ForeignKey(OP, on_delete=CASCADE, related_name='op_serv_ext')
    produto = models.ForeignKey('prod.Prod', on_delete=PROTECT, related_name='prod_serv_ext')
    qtd_programada = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    qtd_realizada = models.DecimalField(default=0, max_digits=13, decimal_places=4)
    qtd_perda = models.DecimalField(default=0, null=True, blank=True, max_digits=13, decimal_places=4)
    nivel = models.IntegerField(default=0)
    prestador_servico = models.ForeignKey('cadastro.Parceiro', on_delete=PROTECT, related_name='operador_serv_ext')
    unidade_tempo = models.CharField(choices = UNIDADE_TEMPO, default='1', max_length=6)
    tempo_estimado = models.DecimalField(default=0, max_digits=13, decimal_places=4)
    momento_ini = models.DateTimeField(null=True, blank=True)
    momento_fim = models.DateTimeField(null=True, blank=True)
    tempo_realizado = models.DecimalField(null=True, blank=True, max_digits=13, decimal_places=4)
    tempo_parada = models.DecimalField(default=0, max_digits=13, decimal_places=4)
    custo_unitario = models.DecimalField(default=0, max_digits=13, decimal_places=4)
    custo_total = models.DecimalField(default=0, max_digits=13, decimal_places=4)

    def __str__(self) -> str:
        return self.produto.desc


'''class OP_servico(models.Model):
    op = models.ForeignKey(OP, on_delete=CASCADE, related_name='op_serv_int')
    produto = models.ForeignKey('prod.Prod', on_delete=PROTECT, related_name='prod_serv_int')
    nivel = models.IntegerField(default=0)
    operador = models.ForeignKey('cadastro.Parceiro', on_delete=PROTECT, related_name='operador_serv_int', null=True, blank=True)
    unidade_tempo = models.CharField(choices = UNIDADE_TEMPO, default='1', max_length=6)
    tempo_estimado = models.DecimalField(default=0, max_digits=13, decimal_places=4)
    momento_ini = models.DateTimeField(null=True, blank=True)
    momento_fim = models.DateTimeField(null=True, blank=True)
    tempo_realizado = models.DecimalField(null=True, blank=True, max_digits=13, decimal_places=4)
    tempo_parada = models.IntegerField(default=0)
    custo_unitario = models.DecimalField(default=0, max_digits=13, decimal_places=4)
    custo_total = models.DecimalField(default=0, max_digits=13, decimal_places=4)


    def __str__(self) -> str:
        return self.produto.produto.desc'''
