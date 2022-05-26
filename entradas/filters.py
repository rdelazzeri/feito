from .models import NF_entrada
import django_filters
from django_filters import CharFilter

class NF_Filter(django_filters.FilterSet):
    num = CharFilter(field_name='num', lookup_expr='icontains', label='Núm. NF')
    #parceiro__nome = django_filters.CharFilter(lookup_expr='icontains')
    parceiro = django_filters.CharFilter(field_name='parceiro__nome', lookup_expr='icontains', label='Fornecedor')
    cidade = django_filters.CharFilter(field_name='parceiro__cidade', lookup_expr='icontains', label='Cidade')
    estado = django_filters.CharFilter(field_name='parceiro__estado', lookup_expr='icontains', label='Estado')
    ano_year__gte = django_filters.NumberFilter(field_name='data_emissao', lookup_expr='year__gte', label='Ano, a partir de:')
    ano_year__lte = django_filters.NumberFilter(field_name='data_emissao', lookup_expr='year__lte', label='Ano, até:')

    class Meta:
        model = NF_entrada

        fields = {
            'operacao': ['exact']
            }

