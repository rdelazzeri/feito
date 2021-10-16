from django import forms
from .models import *
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django.forms import ModelForm, fields


class SearchProdForm(forms.Form):
    cod = forms.CharField(max_length=30, label='Código', required=False)
    desc = forms.CharField(max_length=254, label='Descrição', required=False)

class ProdDetailForm(ModelForm):
     class Meta:
         model = Prod
         fields = '__all__'