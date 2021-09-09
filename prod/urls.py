from django.urls import path

from . import views as v

app_name = 'prod'


urlpatterns = [
    path('', v.prod_list, name='prod_list'),
]