from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Sistema Gerencial DEFER'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('core.urls')),
    path('prod/', include('prod.urls')),
    path('cyber/', include('cyber_sinc.urls')),
    path('com/', include('comercial.urls')),
    path('cad/', include('cadastro.urls')),
    path('pop/', include('modalform.urls')),
    path('fin/', include('financeiro.urls')),
    path('ent/', include('entradas.urls')),
    path('est/', include('estoque.urls')),
    path('pr/', include('producao.urls')),
    path('rel/', include('reports.urls')),
    
]
