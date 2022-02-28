# tutorial/tables.py
import django_tables2 as tables
from django_tables2.utils import A
from .models import Parceiro

class Parc_table(tables.Table):
    
    nome = tables.LinkColumn('cadastro:view_detalhe', args=[A('pk')], orderable=False)
    class Meta:
        model = Parceiro
        template_name = "django_tables2/bootstrap4.html"
        fields = ('nome', 'apelido', 'cnpj', 'municipio', 'estado', 'fone1', 'fone2')
        # add class="paleblue" to <table> tag
        attrs = {'width':'100%'}
        
