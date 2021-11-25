from django.conf.urls import include, url
from django.urls import path
from . import views


urlpatterns = [
    path("l", views.CadView.as_view(), name="cadview"),
    path("", views.lista, name='view_lista'),
    path('<int:id>', views.detalhe, name='view_detalhe'),
    path('muni', views.importMuni, name='view_importMuni'),
    path('p', views.pesq),
    path('s', views.pesquisa),
    path('n', views.novo),
    path('cidades', views.load_cities, name='cidades'),  # <-- this one here
    #url(r'^f/$', views.pf),
    #url(r'^j/$', views.pj),
    #url(r'^s/$', views.pesquisa),
    #url(r'^ds/$', views.pesq),
    #url(r's/(?P<pesq>\w+)$', views.pesquisa, name='view_pesquisa'),
    #url(r'^n/$', views.novo),
    
    #url(r'^c(?P<pk>[0-9]{14})/$', views.detalhe_cnpj, name='view_cnpj'),
]
