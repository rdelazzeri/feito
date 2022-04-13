from django import forms
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

class Label_form(forms.Form):
    
    ini = 'Defer Indústria Metalúrgica'
    emitente = forms.CharField(max_length=60, label='Emitente', required=False, disabled=False, initial=ini, widget=forms.TextInput(attrs={'size': '40'}))
    destinatario = forms.CharField(max_length=60, label='Destinatário', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '40'}))
    num_ped = forms.CharField(max_length=60, label='No Pedido:', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '40'}))
    num_oc = forms.CharField(max_length=60, label='OC Cliente:', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '40'}))
    nf = forms.CharField(max_length=60, label='NF', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '40'}))
    volumes = forms.CharField(max_length=60, label='Volumes', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '40'}))
