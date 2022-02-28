from django.urls import path

from . import views as v

app_name = 'entradas'

urlpatterns = [
    #Notas de entrada
    path('nf/list', v.nf_entrada_list, name = 'nf_entrada_list'),
    path('nf/new', v.nf_entrada_new, name = 'nf_entrada_new'),
    path('nf/read/<int:pk>', v.nf_entrada_read, name = 'nf_entrada_read'),
    path('nf/<int:pk>', v.nf_entrada_detail, name = 'nf_entrada_detail'),
    path('nf/prod_search', v.nf_entrada_prod_search, name = 'nf_entrada_prod_search'),
    path('nf/item_add', v.nf_entrada_item_add, name = 'nf_entrada_item_add'),
    path('nf/item_delete', v.nf_entrada_item_delete, name = 'nf_entrada_item_delete'),
    path('nf/delete/', v.nf_entrada_delete, name = 'nf_entrada_delete'),
    path('nf/parcelas/create', v.nf_entrada_parcelas_create, name = 'nf_entrada_parcelas_create'),
    path('nf/parcelas/delete', v.nf_entrada_parcelas_delete, name = 'nf_entrada_parcelas_delete'),
    path('nome-autocomplete/', v.NomeAutocomplete.as_view(), name='nome-autocomplete'), 
    path('transportadora-autocomplete/', v.TransportadoraAutocomplete.as_view(), name='transportadora-autocomplete'), 

    path('oc/list', v.oc_list, name = 'oc_list'),
    path('oc/new', v.oc_new, name = 'oc_new'),
    path('oc/<int:pk>', v.oc_detail, name = 'oc_detail'),
    path('sm/list', v.sm_list, name = 'sm_list'),
    path('sm/new', v.sm_new, name = 'sm_new'),
    path('sm/<int:pk>', v.sm_detail, name = 'sm_detail'),

]