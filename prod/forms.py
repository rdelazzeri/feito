from django import forms
from .models import *
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django.forms import ModelForm, fields

class CompForm(ModelForm):
    class Meta:
        model = ProdComp
        fields=['codComp.desc', 'qtd',]

