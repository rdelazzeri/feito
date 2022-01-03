from django import forms
from django.forms.widgets import HiddenInput
from .models import *
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Hidden, Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django.forms import ModelForm, fields, Form
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.forms.formsets import BaseFormSet
from decimal import Decimal

class SearchProdForm(forms.Form):
    cod = forms.CharField(max_length=30, label='Código', required=False)
    desc = forms.CharField(max_length=254, label='Descrição', required=False)

class ProdDetailForm(ModelForm):

    class Meta:
        model = Prod
        fields = '__all__'
        exclude = ('codigoProd',)

class ProdCompForm(forms.ModelForm):
    cod = forms.CharField(max_length=30, label='Código', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))
    desc = forms.CharField(max_length=60, label='Componente', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '60'}))
    unid = forms.CharField(max_length=6, label='Unidade', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))
    qtd = forms.CharField(max_length=15, label='Quantidade', required=False, widget=forms.TextInput(attrs={'size': '8'}))
    codComp = forms.CharField(max_length=15, label='Quantidade', required=False, widget=forms.TextInput(attrs={'size': '8'}))

    def __init__(self, *args, **kwargs):
        super(ProdCompForm, self).__init__(*args, **kwargs)
        #super().__init__(*args, **kwargs)
        pr = self.instance
        if pr!=None:
            #cod = pr.codComp.cod
            #desc = pr.codComp.desc
            #unid = pr.codComp.unid.unid
            #qtd = pr.qtd   
            #self.fields['desc'].initial = desc
            #self.fields['unid'].initial = unid
            #self.fields['cod'].initial = cod
            pass

        self.helper = FormHelper
        self.helper.form_tag = False
        self.helper.template = 'prod/table_inline_formset.html'
        self.helper.layout = Layout('cod', 'desc', 'unid', 'qtd' )
            
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

class BaseProdCompFormSet(BaseFormSet):
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
                

               

class ProdCompFormset(forms.Form):
    cod = forms.CharField(max_length=30, label='Código', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))
    desc = forms.CharField(max_length=60, label='Componente', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '60'}))
    unid = forms.CharField(max_length=6, label='Unidade', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))
    qtd = forms.CharField(max_length=15, label='Quantidade', required=False, widget=forms.TextInput(attrs={'size': '8'}))
    codProdComp = forms.CharField(widget = forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(ProdCompFormset, self).__init__(*args, **kwargs)
        self.helper = FormHelper
        self.helper.form_tag = False
        self.helper.template = 'prod/table_inline_formset.html'