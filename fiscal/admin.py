from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(NF_config)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Pre_nota)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Pre_nota_parcelas)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Pre_nota_cliente)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Pre_nota_entrega)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Pre_nota_fatura)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Pre_nota_last_num)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Pre_nota_pedido)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Pre_nota_produtos)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Pre_nota_transporte)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(NFe_transmissao)
class GrupoAdmin(admin.ModelAdmin):
    pass