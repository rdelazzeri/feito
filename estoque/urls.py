from django.urls import path

from . import views as v
app_name = 'estoque'

urlpatterns = [
    path('list', v.estoque_list, name = 'estoque_list'),
    #path('op/new', v.op_new, name = 'op_new'),
    #path('prod/auto', v.ProdutoAutocomplete.as_view(), name = 'produto-autocomplete'),
    #path('op/<int:pk>', v.op_detail, name = 'op_detail'),
    #path('op/detail/delitem', v.op_delitem, name = 'op_delitem'),
    #path('op/comp-fis/add', v.op_comp_fis_add, name = 'op_comp_fis_add'),
    #path('pdf', v.pdf, name = 'pdf'),
    #path('rpt_op/<int:id>', v.rpt_op, name = 'rpt_op'),
]