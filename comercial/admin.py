from django.contrib import admin
from .models import Pedido, Operacao, Vencimento, Pedido_item

@admin.register(Pedido)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Operacao)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Vencimento)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Pedido_item)
class GrupoAdmin(admin.ModelAdmin):
    pass

