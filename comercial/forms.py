from django import forms
#from django.forms.widgets import HiddenInput
from .models import *
#from django.forms.models import inlineformset_factory
#from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Hidden, Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
#from django.forms import ModelForm, fields, Form
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.forms.formsets import BaseFormSet
from decimal import Decimal

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class PedidoModelForm(BSModalModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'

class PedidoItemModelForm(BSModalModelForm):
    class Meta:
        model = Pedido_item
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

        #self.helper.add_input(Submit('submit', 'Submit'))

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

class Pedido_itens_BaseFormSet(BaseFormSet):
    def clean(self): 
        
        if any(self.errors):
           # Don't bother validating the formset unless each form is valid on its own
           print(self.errors)
           return

        for form in self.forms:
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
            if isfloat(form.cleaned_data['pr_unit']):
                qtd = Decimal(form.cleaned_data.get('pr_unit'))
                if qtd < 0:
                    print('erro qtd < 0')
                    raise forms.ValidationError(
                        'A quantidade deve maior ou igual a zero.',
                        code='valor_invalido')
            else:
                raise forms.ValidationError(
                    'A quantidade deve ser um valor numérico.',
                    code='valor_invalido')




class Pedido_itens_formset(forms.Form):
    
    item_id = forms.CharField(max_length=30, label='Código', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '1'}))
    cod = forms.CharField(max_length=30, label='Código', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))
    desc = forms.CharField(max_length=60, label='Descrição', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '60'}))
    unid = forms.CharField(max_length=6, label='Unidade', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))
    qtd = forms.CharField(max_length=15, label='Quantidade', required=False, widget=forms.TextInput(attrs={'size': '8'}))
    pr_unit = forms.CharField(max_length=15, label='Preço Unitário', required=False, widget=forms.TextInput(attrs={'size': '8'}))
    pr_tot = forms.CharField(max_length=15, label='Preço Total', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))
    qtd_entregue = forms.CharField(max_length=30, label='Qtd. Entregue', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))
    val_entregue = forms.CharField(max_length=30, label='Val Faturado', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))
    saldo = forms.CharField(max_length=30, label='Saldo', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))

    '''
    def __init__(self, *args, **kwargs):
        super(Pedido_itens_formset, self).__init__(*args, **kwargs)
        self.helper = FormHelper
        self.helper.form_tag = False
        #self.helper.template = 'prod/table_inline_formset.html'
    '''
