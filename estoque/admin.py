from django.contrib import admin
from .models import Movimento

@admin.register(Movimento)
class GrupoAdmin(admin.ModelAdmin):
    pass