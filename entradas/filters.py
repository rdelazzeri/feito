from .models import NF_entrada
import django_filters


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = NF_entrada
        fields = ['num', 'parceiro']