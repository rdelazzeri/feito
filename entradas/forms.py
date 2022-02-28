from django import forms

from .models import *
from crispy_forms.layout import Button, Hidden, Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.forms.formsets import BaseFormSet
from decimal import Decimal
from django.forms import Form, ModelForm, DateField, widgets
from core.services import *
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from dal import autocomplete
from financeiro.models import Conta_pagar
import djhacker

''''
djhacker.formfield(
    NF_entrada.parceiro,
    forms.ModelChoiceField,
    widget=autocomplete.ModelSelect2(
        url='entradas:nome-autocomplete',
        attrs={
        # Only trigger autocompletion after 3 characters have been typed
        'data-minimum-input-length': 3,
        },
        )
)
'''

class NF_entrada_detail_form(forms.ModelForm):
    class Meta:
        model = NF_entrada
        fields = '__all__' 
        widgets = {
            'parceiro': autocomplete.ModelSelect2(
                url='entradas:nome-autocomplete',
                attrs={'data-minimum-input-length': 3,
                },
                ),
            'transportadora': autocomplete.ModelSelect2(
                url='cadastro:transportadora-autocomplete',
                attrs={'data-minimum-input-length': 3,},
                ),
        }

class NF_entrada_itens_BaseFormSet(BaseFormSet):
    def clean(self): 
        if any(self.errors):
           # Don't bother validating the formset unless each form is valid on its own
           print(self.errors)
           return

        for form in self.forms:
            #print(form)
            try:
                if isfloat(form.cleaned_data['qtd']):
                    qtd = Decimal(form.cleaned_data.get('qtd'))
                    if qtd < 0:
                        print('erro qtd < 0')
                        raise forms.ValidationError(
                            'A quantidade deve maior ou igual a zero.',
                            code='valor_invalido')
                else:
                    raise forms.ValidationError(
                        'A quantidade deve ser um valor numérico.',
                        code='valor_invalido')
                if isfloat(form.cleaned_data['preco_unit']):
                    pr_unit = Decimal(form.cleaned_data.get('preco_unit'))
                    if pr_unit < 0:
                        print('erro pr_unit < 0')
                        raise forms.ValidationError(
                            'O preço deve maior ou igual a zero.',
                            code='valor_invalido')
                else:
                    raise forms.ValidationError(
                        'O preço deve ser um valor numérico.',
                        code='valor_invalido')
            except:
                print('erro')

class NF_entrada_itens_formset(forms.Form):
    
    item_id = forms.CharField(max_length=30, label='Código', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '1'}))
    cod = forms.CharField(max_length=30, label='Código', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))
    desc = forms.CharField(max_length=60, label='Descrição', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '60'}))
    unid = forms.CharField(max_length=6, label='Unidade', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '7'}))
    qtd = forms.CharField(max_length=15, label='Quantidade', required=False, widget=forms.TextInput(attrs={'size': '7'}))
    preco_unit = forms.CharField(max_length=15, label='Preço Unitário', required=False, widget=forms.TextInput(attrs={'size': '7'}))
    preco_tot = forms.CharField(max_length=15, label='Preço Total', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '7'}))
    aliq_icms = forms.CharField(max_length=15, label='% ICMS', required=False, widget=forms.TextInput(attrs={'size': '7'}))
    aliq_ipi = forms.CharField(max_length=15, label='% IPI', required=False, widget=forms.TextInput(attrs={'size': '7'}))
    valor_icms = forms.CharField(max_length=15, label='Val. ICMS', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '7'}))
    valor_ipi = forms.CharField(max_length=15, label='Val. IPI', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '7'}))
    valor_total_item = forms.CharField(max_length=15, label='Total', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '7'}))



class NF_entrada_parcelas_BaseFormSet(BaseFormSet):
    def clean(self): 
        print('base formset parcelas')
        if any(self.errors):
           # Don't bother validating the formset unless each form is valid on its own
           print(self.errors)
           return

        for form in self.forms:
            print(form.cleaned_data['parc_id'])
            


class NF_entrada_parcelas_formset(forms.Form):
    parc_id = forms.CharField(max_length=30, label='ID', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))
    num = forms.IntegerField(label='Número', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))
    venc = forms.DateField(label='Vencimento', required=False, disabled=False, widget=forms.DateInput(attrs={'size': '8'}))
    valor = forms.CharField(max_length=60, label='Valor', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '8'}))

