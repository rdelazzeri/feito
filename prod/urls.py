from django.urls import path

from . import views as v

app_name = 'prod'

urlpatterns = [
    path('', v.prod_detail, name = 'prod_detail'),
    path('s', v.prod_list, name = 'prod_list'),
    path('n', v.prod_new, name = 'prod_new'),
   #path('del', v.prod_delete, name = 'prod_delete'),
    path('comp/<produto_id>', v.prod_comp, name='prod_comp'),
    path('search', v.prod_search, name = 'prod_search'),
    path('prodSearch', v.produto_search, name = 'produto_search'),
    path('p<prod_id>', v.prod_detail, name = 'prod_detail'),
    path('print_comp/<prod>', v.print_comp, name = 'print_comp'),
    #path('prodcompup', v.Prod_Update, name = 'prod_update'),
    #path('sinc_unid', v.cyber_sinc_unid, name = 'cyber_sinc_unid '),
    #path('sinc_ncm', v.cyber_sinc_ncm, name = 'cyber_sinc_ncm'),

]