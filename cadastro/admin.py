from django.contrib import admin
from .models import Parceiro, Tipo_parceiro, Estado, Municipio
# Register your models here.

@admin.register(Parceiro)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Tipo_parceiro)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Estado)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(Municipio)
class GrupoAdmin(admin.ModelAdmin):
    pass