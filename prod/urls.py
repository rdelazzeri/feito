from django.urls import path

from . import views as v

app_name = 'prod'

urlpatterns = [
    path('', v.prod_list, name = 'prod_list'),
    path('prodcomp', v.Prod_Create, name = 'prod_create'),
    path('prodcompup', v.Prod_Update, name = 'prod_update'),
    #path('sinc_unid', v.cyber_sinc_unid, name = 'cyber_sinc_unid '),
    #path('sinc_ncm', v.cyber_sinc_ncm, name = 'cyber_sinc_ncm'),
]