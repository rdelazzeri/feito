from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from comercial.models import Entrega
from cadastro.models import Parceiro
from prod.models import Prod
from entradas.models import NF_entrada_itens
from decimal import Decimal
import datetime
from django.db.models import Avg, Count, Min, Sum



from django.db.models.signals import pre_delete
from django.dispatch import receiver

class MovimentoManager(models.Manager):
    def movimento_save(self, dados):
        print('entrei em movimento save')
        #mov, created = Movimento.objects.get_or_create(tipo = dados['tipo'], chave = int(dados['chave']))            
        mov = Movimento()
        mov.data = dados['data']
        mov.desc = dados['desc'] 
        mov.produto = dados['produto']
        mov.qtd_entrada = dados['qtd_entrada']
        mov.qtd_saida = dados['qtd_saida']
        mov.valor = dados['valor']
        mov.tipo = dados['tipo']
        mov.chave = dados['chave']
        #saldo = Decimal(mov.produto.qEstoque) + Decimal(mov.qtd_entrada) - Decimal(mov.qtd_saida)
        #mov.produto.qEstoque = saldo
        #mov.qtd_saldo = saldo
        #mov.produto.save()
        #mov.save()
        print('conclui movimento save')
        #return super().save()


    def estorno_estoque(self, chave, tipo):
        print('cheguei no estorno estoque model')
        #mov, created = Movimento.objects.get_or_create(tipo = dados['tipo'], chave = int(dados['chave']))            
        #itens = Movimento.objects.filter(chave=chave, tipo=tipo)
        itens = Movimento.objects.filter(chave=chave, tipo=tipo).values('produto', 'valor').annotate(Sum('qtd_entrada')).annotate(Sum('qtd_saida'))
        for it in itens:
            print(it)
            s = it['qtd_saida__sum']
            e = it['qtd_entrada__sum']
            saldo = e - s
            if saldo != 0:
                if saldo < 0:
                    qe = saldo * -1
                    qs = 0
                else:
                    qe = 0
                    qs = saldo

                prod = Prod.objects.get(id = it['produto'])
                mov = Movimento()
                mov.data = datetime.date.today()
                mov.desc = 'Estorno id_mov - tipo: %s id: %s' %(tipo, chave)
                mov.produto = prod
                mov.qtd_entrada = qe
                mov.qtd_saida = qs
                mov.valor = it['valor']
                mov.tipo = tipo
                mov.chave = chave
                saldo = Decimal(mov.produto.qEstoque) + Decimal(mov.qtd_entrada) - Decimal(mov.qtd_saida)
                mov.produto.qEstoque = saldo
                mov.qtd_saldo = saldo
                mov.produto.save()
                mov.save()


    def movimento_delete(self, tipo, chave):
        try:
            mov = Movimento.objects.get(tipo = tipo, chave = chave)
            mov.produto.qEstoque = mov.produto.qEstoque + mov.qtd_saida - mov.qtd_entrada
            mov.produto.save()
            mov.delete()
        except:
            pass
        

class Movimento(models.Model):
    data = models.DateField(null=True, blank=True)
    desc = models.CharField(max_length=100, null=True, blank=True)
    produto = models.ForeignKey(Prod, on_delete=PROTECT, null=True, blank=True)
    tipo = models.CharField(max_length=4, default='')
    chave = models.BigIntegerField(default=0)
    qtd_entrada = models.DecimalField(max_digits=13, decimal_places=3, default=0)
    qtd_saida = models.DecimalField(max_digits=13, decimal_places=3, default=0)
    qtd_saldo = models.DecimalField(max_digits=13, decimal_places=3, default=0)
    valor = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    objects = MovimentoManager()

    def __str__(self) -> str:
        return self.desc

    def save(self, *args, **kwargs):
        #qtd = Decimal(self.produto.qEstoque) + Decimal(self.qtd_entrada) - Decimal(self.qtd_saida)
        #self.produto.qEstoque = qtd
        #self.qtd_saldo = qtd
        return super().save()

