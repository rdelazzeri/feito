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
    path('new/search_table', v.pedidos_prod_search_table, name='pedidos_prod_search_table'),
    path('pedidos/', v.pedidos, name='pedidos'),
    path('pedido_add_item/', v.Pedido_add_item.as_view(), name='pedido_add_item'),
    
    #Pedido
    path('pedido/new/', v.pedido_new, name='pedido_new'),
    path('pedido_full/<pedido_id>', v.pedido_full, name = 'pedido_full'),
    path('pedido_full/search/', v.pedidos_prod_search, name='pedidos_prod_search'),
    path('pedido_full/prod_selected/', v.pedido_item_add, name='pedido_item_add'),
    path('pedido_full/item_delete/', v.pedido_item_delete, name='pedido_item_delete'),
    path('pedido_full/create/', v.pedido_new, name='pedido_new'),
    path('pedido_full/entrega_add/', v.pedido_entrega_add, name='pedido_entrega_add'),
    #path('pedido_full/testaJson/', v.pedido_testaJson, name='pedido_testaJson'),

    #Orçamento
    path('orcamento/new/', v.orcamento_new, name='orcamento_new'),
    path('orcamento/list/', v.orcamento_list, name='orcamento_list'),
    path('orcamento/detail/<orcamento_id>', v.orcamento_detail, name = 'orcamento_detail'),
    path('orcamento/prod_search', v.orcamento_prod_search, name = 'orcamento_prod_search'),
    path('orcamento/item_add', v.orcamento_item_add, name = 'orcamento_item_add'),
    path('orcamento/item_delete', v.orcamento_item_delete, name = 'orcamento_item_delete'),
    path('orcamento/delete/', v.orcamento_delete, name = 'orcamento_delete'),
    path('orcamento/pedido_add', v.orcamento_pedido_add, name = 'orcamento_pedido_add'),
    
    #Entega
    path('entrega/new/', v.entrega_new, name='entrega_new'),
    path('entrega/list/', v.entrega_list, name='entrega_list'),
    path('entrega/detail/<entrega_id>', v.entrega_detail, name = 'entrega_detail'),
    path('entrega/prod_search', v.entrega_prod_search, name = 'entrega_prod_search'),
    path('entrega/item_add', v.entrega_item_add, name = 'entrega_item_add'),
    path('entrega/item_delete', v.entrega_item_delete, name = 'entrega_item_delete'),
    path('entrega/delete/', v.entrega_delete, name = 'entrega_delete'),
    path('entrega/pre_nota_add', v.pre_nota_add, name = 'pre_nota_add'),
    path('entrega/pre_nota_retorno', v.pre_nota_retorno, name = 'pre_nota_retorno'),
    path('entrega/pre_nota_estorno', v.pre_nota_estorno, name = 'pre_nota_estorno'),
    path('entrega/label', v.label, name = 'label'),
]