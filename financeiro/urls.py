from django.urls import path

from . import views as v

app_name = 'financeiro'

urlpatterns = [
    path('cp/list', v.cp_list, name = 'cp_list'),
    path('cp/filter', v.cp_filter, name = 'cp_filter'),
    path('cp/lote', v.cp_lote, name = 'cp_lote'),
    path('cp/new', v.cp_new, name = 'cp_new'),
    path('cp/detail/<int:pk>', v.cp_detail, name = 'cp_detail'),
    path('parc-autocomplete/', v.ParcAutocomplete.as_view(), name='parc-autocomplete'),
    path('entrada-autocomplete/', v.EntradaAutocomplete.as_view(), name='entrada-autocomplete'),
    
    #CR
    path('cr/list', v.cr_list, name = 'cr_list'),
    path('cr/filter', v.cr_filter, name = 'cr_filter'),
    path('cr/lote', v.cr_lote, name = 'cr_lote'),
    path('cr/new', v.cr_new, name = 'cr_new'),
    path('cr/detail/<int:pk>', v.cr_detail, name = 'cr_detail'),
    path('parc-autocomplete/', v.ParcAutocomplete.as_view(), name='parc-autocomplete'),
    path('entrega-autocomplete/', v.EntregaAutocomplete.as_view(), name='entrega-autocomplete'),


]