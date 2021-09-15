from django.contrib import admin
from .models import Grupo, Prod, Produto, Unid, NCM

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

@admin.register(Prod)
class GrupoAdmin(admin.ModelAdmin):
    pass

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
