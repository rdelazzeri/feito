from .models import Entrega
import django_filters
from django_filters import CharFilter

class Entregas_Filter(django_filters.FilterSet):
    num = CharFilter(field_name='num', lookup_expr='icontains', label='Núm. Entrega')
    num_nf = CharFilter(field_name='num_nf', lookup_expr='icontains', label='Núm. NF')
    cliente = django_filters.CharFilter(field_name='cliente__nome', lookup_expr='icontains', label='Cliente')
    cidade = django_filters.CharFilter(field_name='cliente__cidade', lookup_expr='icontains', label='Cidade')
    estado = django_filters.CharFilter(field_name='cliente__estado', lookup_expr='icontains', label='Estado')
    ano_year__gte = django_filters.NumberFilter(field_name='data_emissao', lookup_expr='year__gte', label='Ano, a partir de:')
    ano_year__lte = django_filters.NumberFilter(field_name='data_emissao', lookup_expr='year__lte', label='Ano, até:')

    class Meta:
        model = Entrega

        fields = {
            'operacao': ['exact']
            }

