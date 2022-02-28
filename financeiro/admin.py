from django.contrib import admin
from .models import * 

@admin.register(Plano_contas, Status, Banco, Origem, Conta_receber, Conta_pagar, Diario, Vencimento )
class GrupoAdmin(admin.ModelAdmin):
    pass
