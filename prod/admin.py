from django.contrib import admin
from .models import Grupo, Prod, ProdComp, Produto, Unid, NCM, TipoProduto, OrigemFiscal

# Register your models here.

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Unid)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(NCM)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(TipoProduto)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(OrigemFiscal)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(ProdComp)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Prod)
class GrupoAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'cod',
        'desc',
        'unid',
        'qEstoque',
        'grupo',
    )
    search_fields = ('desc', 'cod',)
    list_filter = ('grupo',)



'''
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'importado',
        'ncm',
        'preco',
        'estoque',
        'estoque_minimo',
    )
    search_fields = ('produto',)
    list_filter = ('importado',)
'''

