from django.contrib import admin
from .models import CC, Conta

# Register your models here.
@admin.register(Conta)
class GrupoAdmin(admin.ModelAdmin):
    pass

@admin.register(CC)
class GrupoAdmin(admin.ModelAdmin):
    pass