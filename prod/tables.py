import django_tables2 as tables

class SincTable(tables.Table):
    num = tables.Column()
    cod = tables.Column()
    descricao = tables.Column()

