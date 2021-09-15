from django.urls import path

from . import views as v

app_name = 'prod'

urlpatterns = [
    path('', v.prod_list, name = 'prod_list'),
    path('cyber/sinc', v.prod_sinc_cyber, name = 'prod_sinc_cyber'),
    path('cyber/sinc_grupos', v.cyber_sinc_grupos, name = 'cyber_sinc_grupos')
]