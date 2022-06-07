from django.urls import path

from . import views as v

app_name = 'financeiro'

urlpatterns = [
    path('cp/list', v.cp_list, name = 'cp_list'),
    path('cp/new', v.cp_new, name = 'cp_new'),
    path('cp/detail/<int:pk>', v.cp_detail, name = 'cp_detail'),
    path('cr/list', v.cr_list, name = 'cr_list'),
    path('parc-autocomplete/', v.ParcAutocomplete.as_view(), name='parc-autocomplete'),
    path('entrada-autocomplete/', v.EntradaAutocomplete.as_view(), name='entrada-autocomplete'),

]