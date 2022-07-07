from .models import Conta_pagar, Conta_receber
import django_filters
from django_filters import CharFilter

class CP_Filter(django_filters.FilterSet):
    nf_num = CharFilter(field_name='num', lookup_expr='icontains', label='Núm. NF')
    num_nf = CharFilter(field_name='num_nf', lookup_expr='icontains', label='Núm. NF')
    cliente = django_filters.CharFilter(field_name='parceiro__nome', lookup_expr='icontains', label='parceiro')
    cidade = django_filters.CharFilter(field_name='parceiro__cidade', lookup_expr='icontains', label='parceiro')
    estado = django_filters.CharFilter(field_name='parceiro__estado', lookup_expr='icontains', label='parceiro')
    data_emi__gte = django_filters.NumberFilter(field_name='data_emissao', lookup_expr='gte', label='Data de emissão, a partir de:')
    data_emi__lte = django_filters.NumberFilter(field_name='data_emissao', lookup_expr='lte', label='Data de emissão, até:')
    data_venc__gte = django_filters.NumberFilter(field_name='data_vencimento', lookup_expr='gte', label='Data de vencimento, a partir de:')
    data_venc__lte = django_filters.NumberFilter(field_name='data_vencimento', lookup_expr='lte', label='Data de vencimento, até:')
    data_pgto__gte = django_filters.NumberFilter(field_name='data_pagamento', lookup_expr='gte', label='Data de pagamento, a partir de:')
    data_pgto__lte = django_filters.NumberFilter(field_name='data_pagamento', lookup_expr='lte', label='Data de pagamento, até:')
    class Meta:
        model = Conta_pagar

        fields = {
            'conta_caixa': ['exact'],
            'status':['exact']
            }

class CR_Filter(django_filters.FilterSet):
    parcela_num = CharFilter(field_name='parcela_num', lookup_expr='icontains', label='Parcela num:')
    nf_num = CharFilter(field_name='nf_num', lookup_expr='icontains', label='NF num:')
    cliente = django_filters.CharFilter(field_name='parceiro__nome', lookup_expr='icontains', label='Cliente')
    cidade = django_filters.CharFilter(field_name='parceiro__cidade', lookup_expr='icontains', label='Cidade')
    estado = django_filters.CharFilter(field_name='parceiro__estado', lookup_expr='icontains', label='Estado')
    data_emi__gte = django_filters.NumberFilter(field_name='data_emissao', lookup_expr='gte', label='Data de emissão, a partir de:')
    data_emi__lte = django_filters.NumberFilter(field_name='data_emissao', lookup_expr='lte', label='Data de emissão, até:')
    data_venc__gte = django_filters.NumberFilter(field_name='data_vencimento', lookup_expr='gte', label='Data de vencimento, a partir de:')
    data_venc__lte = django_filters.NumberFilter(field_name='data_vencimento', lookup_expr='lte', label='Data de vencimento, até:')
    data_pgto__gte = django_filters.NumberFilter(field_name='data_pagamento', lookup_expr='gte', label='Data de pagamento, a partir de:')
    data_pgto__lte = django_filters.NumberFilter(field_name='data_pagamento', lookup_expr='lte', label='Data de pagamento, até:')
    class Meta:
        model = Conta_receber

        fields = {
            'conta_caixa': ['exact'],
            'status':['exact']
            }
