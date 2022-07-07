from django import forms
#from django.forms.widgets import HiddenInput
from .models import *
#from django.forms.models import inlineformset_factory
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Button, Hidden, Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django.forms import ModelForm, fields, Form
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Layout, Submit, Row, Column
#from django.forms.formsets import BaseFormSet
#from decimal import Decimal
from dal import autocomplete

CP_OPCOES = (
    ('0','Ações em lote'),
    ('1','Baixar com data de hoje'),
    ('2','Baixar com data do vencimento'),
    ('3', 'Somar')
)


class CP_detail_form(ModelForm):
    
    #entrada = forms.CharField(max_length=60, label='Nota de entrada', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '60'}))

    class Meta:
        model = Conta_pagar
        fields = '__all__'
        widgets = {
            'parceiro': autocomplete.ModelSelect2(
                url='cadastro:nome-autocomplete',
                attrs={'data-minimum-input-length': 3,
                        'dropdownAutoWidth': True,
                },
                ),
            'entrada': autocomplete.ModelSelect2(
                url='financeiro:entrada-autocomplete',
                attrs={'data-minimum-input-length': 3,
                        'dropdownAutoWidth': True,
                },
                ),
            
        }

class CP_acoes_lote_form(Form):
    opcoes = forms.ChoiceField(choices = CP_OPCOES, label="")


CR_OPCOES = (
    ('0','Ações em lote'),
    ('1','Baixar com data de hoje'),
    ('2','Baixar com data do vencimento'),
    ('3','Emitir Boleto Banrisul'),
    ('4','Enviar XML por e-mail'),
    ('3', 'Somar')
)

class CR_acoes_lote_form(Form):
    opcoes = forms.ChoiceField(choices = CR_OPCOES, label="")

class CR_detail_form(ModelForm):
    
    #entrada = forms.CharField(max_length=60, label='Nota de entrada', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '60'}))

    class Meta:
        model = Conta_receber
        fields = '__all__'
        widgets = {
            'parceiro': autocomplete.ModelSelect2(
                url='cadastro:nome-autocomplete',
                attrs={'data-minimum-input-length': 3,
                        'dropdownAutoWidth': True,
                },
                ),
            'entrega': autocomplete.ModelSelect2(
                url='financeiro:entrega-autocomplete',
                attrs={'data-minimum-input-length': 3,
                        'dropdownAutoWidth': True,
                },
                ),
            
        }

