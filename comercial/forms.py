from django import forms
#from django.forms.widgets import HiddenInput
from .models import *
#from django.forms.models import inlineformset_factory
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Button, Hidden, Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
#from django.forms import ModelForm, fields, Form
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
#from django.forms.formsets import BaseFormSet
#from decimal import Decimal

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class PedidoModelForm(BSModalModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'


class PedidoFilterForm(BSModalForm):
    cliente = forms.CharField()
    tipo_frete = forms.CharField()

    class Meta:
        fields = ['cliente', 'tipo_frete']


class PedidoDetailForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))