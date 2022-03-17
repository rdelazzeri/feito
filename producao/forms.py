from random import choices
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

class OP_detail_form(forms.ModelForm):

    qtd_producao = forms.CharField(max_length=15, label='Qtd producao', required=False, widget=forms.TextInput(attrs={'size': '7'}))
    qtd_perdida = forms.CharField(max_length=15, label='Qtd perda', required=False, widget=forms.TextInput(attrs={'size': '7'}))
    data_producao = forms.DateField(label='Data producao', required=False, widget=forms.DateInput())

    class Meta:
        model = OP
        fields = '__all__' 
        widgets = {
            'produto': autocomplete.ModelSelect2(
                url='producao:produto-autocomplete',
                attrs={'data-minimum-input-length': 3,
                },
                ),
        }

class OP_comp_fis_BaseFormSet(BaseFormSet):
    def clean(self): 
        if any(self.errors):
           # Don't bother validating the formset unless each form is valid on its own
           print(self.errors)
           return

        for form in self.forms:
            #print(form)
            try:
                pass
            except:
                print('erro')

class OP_comp_fis_formset(forms.Form):
    
    item_id = forms.CharField(max_length=30, label='Código', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '1'}))
    source = forms.CharField(max_length=30, label='Código', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '1'}))
    cod = forms.CharField(max_length=30, label='Código', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))
    desc = forms.CharField(max_length=60, label='Descrição', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '60'}))
    unid = forms.CharField(max_length=6, label='Unidade', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '7'}))
    qtd_programada = forms.CharField(max_length=15, label='Quantidade', required=False, widget=forms.TextInput(attrs={'size': '7'}))
    custo_unit = forms.CharField(max_length=15, label='Custo Unitário', required=False, widget=forms.TextInput(attrs={'size': '7'}))
    custo_tot = forms.CharField(max_length=15, label='Custo Total', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '7'}))



class OP_serv_int_BaseFormSet(BaseFormSet):
    def clean(self): 
        if any(self.errors):
           # Don't bother validating the formset unless each form is valid on its own
           print(self.errors)
           return

        for form in self.forms:
            #print(form)
            try:
                pass
            except:
                print('erro')

SOURCE = (
    ('SI', 'SI'),
    ('SE', 'SE'),
    ('CF', 'CF'),
)

class OP_serv_int_formset(forms.Form):

    oper = Parceiro.objects.filter(tipo__sigla = 'OP')
    
    item_id = forms.CharField(max_length=30, label='Código', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '1'}))
    source = forms.CharField(max_length=30, label='Código', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '1'}))
    nivel = forms.CharField(max_length=30, label='Nível', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '1'}))
    cod = forms.CharField(max_length=30, label='Código', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))
    desc = forms.CharField(max_length=60, label='Descrição', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '60'}))
    unid = forms.CharField(max_length=6, label='Unidade', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '7'}))
    tempo_estimado = forms.CharField(max_length=15, label='Quantidade', required=False, widget=forms.TextInput(attrs={'size': '7'}))
    custo_unit = forms.CharField(max_length=15, label='Custo Unitário', required=False, widget=forms.TextInput(attrs={'size': '7'}))
    custo_tot = forms.CharField(max_length=15, label='Custo Total', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '7'}))
    operador = forms.ModelChoiceField(queryset=oper)
    source = forms.ChoiceField(choices=SOURCE, label='Tipo', required=False, disabled=False)