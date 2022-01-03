from .models import Pedido
import django_tables2 as tables
from django_tables2.utils import A 

class PedidosTable(tables.Table):
    num = tables.LinkColumn('comercial:pedido_detail', args=[A('pk')])
    cliente = tables.Column()
    operacao = tables.Column()
