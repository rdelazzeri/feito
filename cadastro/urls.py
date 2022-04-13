from django.conf.urls import include, url
from django.urls import path
from . import views

app_name = 'cadastro'

urlpatterns = [
    path("l", views.CadView.as_view(), name="cadview"),
    path("", views.lista, name='view_lista'),
    path('<int:id>', views.detalhe, name='view_detalhe'),
    path('muni', views.importMuni, name='view_importMuni'),
    path('p', views.pesq),
    path('s', views.pesquisa),
    path('n', views.novo),
    path('cidades', views.load_cities, name='cidades'),
    path('nome-autocomplete/', views.NomeAutocomplete.as_view(), name='nome-autocomplete'), 
    path('transportadora-autocomplete/', views.TransportadoraAutocomplete.as_view(), name='transportadora-autocomplete'), 

]
