from django.urls import path

from . import views as v

app_name = 'caixa'

urlpatterns = [
    path('', v.cx_list, name = 'cx_list'),


]