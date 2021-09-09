from django.contrib import admin
from .models import Estoque, EstoqueItens

class EstoqueItensInLine(admin.TabularInline):
    model = EstoqueItens
    extra = 0

@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    inlines = (EstoqueItensInLine,)
    list_display = (
        '__str__',
        'nf',
        'funcionario'
    )
    search_fields = ('nf',)
    list_filter = ('funcionario',)
    date_hierarchy = 'created'
# Register your models here.