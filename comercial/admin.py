from django.contrib import admin
from .models import Orcamento, Orcamento_item, Orcamento_origem, Orcamento_status, Pedido, Operacao, Vencimento, Pedido_item, Comercial_config, Entrega, Entrega_item, Entrega_parcelas

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

@admin.register(Orcamento)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Orcamento_item)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Orcamento_status)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Orcamento_origem)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Comercial_config, Entrega, Entrega_item, Entrega_parcelas )
class GrupoAdmin(admin.ModelAdmin):
    pass