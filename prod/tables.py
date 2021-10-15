from prod.models import ProdComp, Prod
import django_tables2 as tables

class SincTable(tables.Table):
    num = tables.Column()
    cod = tables.Column()
    descricao = tables.Column()

class CompTable(tables.Table):
    class meta():
        model = ProdComp

class ProdTable(tables.Table):
    class meta():
        model = Prod