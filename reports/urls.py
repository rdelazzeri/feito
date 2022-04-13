from django.urls import path

from . import views as v

app_name = 'reports'

urlpatterns = [
    #Notas de entrada
    path('label/', v.label, name = 'label'),


]