from django.contrib import admin
from .models import *

@admin.register(Operacao_entrada, NF_entrada, NF_entrada_itens, Ordem_compra, Ordem_compra_itens, Solicitacao_material, Solicitacao_material_item)
class AuthorAdmin(admin.ModelAdmin):
    pass
