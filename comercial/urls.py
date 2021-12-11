from django.urls import path

from . import views as v

app_name = 'comercial'

urlpatterns = [
    path('', v.pedidos_list, name = 'pedidos_list'),
    path('detail/<ped_id>', v.pedido_detail, name = 'pedido_detail'),
    path('read/<int:pk>', v.Pedido_read.as_view(), name = 'pedido_read'),
    path('update/<int:pk>', v.Pedido_update.as_view(), name='pedido_update'),
    path('delete/<int:pk>', v.Pedido_delete.as_view(), name='pedido_delete'),
    path('filter/', v.Pedido_filter.as_view(), name='pedido_filter'),
    path('create/', v.Pedido_create.as_view(), name='pedido_create'),
    path('new/', v.pedido_new, name='pedido_new'),
    #path('new/search', v.pedidos_prod_search, name='pedidos_prod_search'),
    path('new/search_table', v.pedidos_prod_search_table, name='pedidos_prod_search_table'),
    path('pedidos/', v.pedidos, name='pedidos'),
    path('pedido_add_item/', v.Pedido_add_item.as_view(), name='pedido_add_item'),
    path('pedido_full/<pedido_id>', v.pedido_full, name = 'pedido_full'),
    path('pedido_full/search/', v.pedidos_prod_search, name='pedidos_prod_search'),
    #path('pedido_full/search/prod/<produto><pedido>', v.pedidos_prod_search3, name='pedidos_prod_search3'),
    path('pedido_full/prod_selected/', v.pedidos_prod_search3, name='pedidos_prod_selected'),
    path('pedido_full/item_delete/', v.pedido_item_delete, name='pedido_item_delete'),
]