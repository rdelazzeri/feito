from django.contrib import admin
from .models import Grupo, SubGrupo, Prod, ProdComp, Unid, NCM, TipoProduto, OrigemFiscal

# Register your models here.

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(SubGrupo)
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


