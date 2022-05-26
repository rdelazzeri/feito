from django.urls import path

from . import views as v

app_name = 'financeiro'

urlpatterns = [
    path('cp/list', v.cp_list, name = 'cp_list'),
    path('cp/detail/<id>', v.cp_detail, name = 'cp_detail'),
    path('cr/list', v.cr_list, name = 'cr_list'),

]