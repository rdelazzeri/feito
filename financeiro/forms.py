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


class CP_detail_form(ModelForm):
    
    #entrada = forms.CharField(max_length=60, label='Nota de entrada', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '60'}))

    class Meta:
        model = Conta_pagar
        fields = '__all__'
        widgets = {
            'parceiro': autocomplete.ModelSelect2(
                url='cadastro:nome-autocomplete',
                attrs={'data-minimum-input-length': 3,
                },
                ),
            'entrada': autocomplete.ModelSelect2(
                url='financeiro:entrada-autocomplete',
                attrs={'data-minimum-input-length': 3,
                },
                ),
            
        }