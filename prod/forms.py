from django import forms
from .models import *
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit


class CompForm(forms.Form):
    codComp = forms.CharField()
    qtd = forms.DecimalField(decimal_places=3, max_digits=12)

    