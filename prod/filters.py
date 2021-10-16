import django_filters
from .models import Prod


class ProdFilter(django_filters.FilterSet):
    class Meta:
        model = Prod
        fields = {
            'cod': ['istartswith'],
            'desc': ['icontains'],
        }
