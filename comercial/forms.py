from django import forms

#from django.forms.widgets import HiddenInput
from .models import *
from fiscal.models import NFe_transmissao
#from django.forms.models import inlineformset_factory
#from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Hidden, Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
#from django.forms import ModelForm, fields, Form
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.forms.formsets import BaseFormSet
from decimal import Decimal
from core.services import *
from django.forms import Form, ModelForm, DateField, widgets
from dal import autocomplete
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

#--------------------------------------
#
#orçamento
#
#--------------------------------------
class OrcamentoDetailForm(forms.ModelForm):
    class Meta:
        model = Orcamento
        fields = '__all__' 
        widgets = {
            'cliente': autocomplete.ModelSelect2(
                url='cadastro:nome-autocomplete',
                attrs={'data-minimum-input-length': 3,
                },
                ),
            'transportadora': autocomplete.ModelSelect2(
                url='cadastro:transportadora-autocomplete',
                attrs={'data-minimum-input-length': 3, 'size': '3'},
                ),
        }


class Orcamento_itens_BaseFormSet(BaseFormSet):
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
                pr_unit = Decimal(form.cleaned_data.get('pr_unit'))
                if pr_unit < 0:
                    print('erro pr_unit < 0')
                    raise forms.ValidationError(
                        'O preço deve maior ou igual a zero.',
                        code='valor_invalido')
            else:
                raise forms.ValidationError(
                    'O preço deve ser um valor numérico.',
                    code='valor_invalido')

class Orcamento_itens_formset(forms.Form):
    
    item_id = forms.CharField(max_length=30, label='Código', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '1'}))
    cod = forms.CharField(max_length=30, label='Código', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))
    desc = forms.CharField(max_length=60, label='Descrição', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '60'}))
    unid = forms.CharField(max_length=6, label='Unidade', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))
    qtd = forms.CharField(max_length=15, label='Quantidade', required=False, widget=forms.TextInput(attrs={'size': '8'}))
    pr_unit = forms.CharField(max_length=15, label='Preço Unitário', required=False, widget=forms.TextInput(attrs={'size': '8'}))
    pr_tot = forms.CharField(max_length=15, label='Preço Total', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))
    obs = forms.CharField(max_length=500, label='Qtd. Entregue', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '40'}))


#--------------------------------------
#
#pedido
#
#--------------------------------------
class PedidoDetailForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
        widgets = {
            'cliente': autocomplete.ModelSelect2(
                url='cadastro:nome-autocomplete',
                attrs={'data-minimum-input-length': 3,
                },
                ),
            'transportadora': autocomplete.ModelSelect2(
                url='cadastro:transportadora-autocomplete',
                attrs={'data-minimum-input-length': 3,},
                ),
        }




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
    qtd_saldo = forms.CharField(max_length=30, label='Saldo', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))
    valor_saldo = forms.CharField(max_length=30, label='Saldo', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '8'}))

    '''
    def __init__(self, *args, **kwargs):
        super(Pedido_itens_formset, self).__init__(*args, **kwargs)
        self.helper = FormHelper
        self.helper.form_tag = False
        #self.helper.template = 'prod/table_inline_formset.html'
    '''



#--------------------------------------
#
#Entrega
#
#--------------------------------------
class EntregaDetailForm(forms.ModelForm):
    num_nf = forms.CharField(disabled=True)
    num = forms.CharField(disabled=True)
    data_cadastro = forms.CharField(disabled=True)
    data_emissao = forms.CharField(disabled=True)
    valor_total_produtos = forms.CharField(disabled=True)
    valor_total_entrega = forms.CharField(disabled=True)
    #status = forms.ChoiceField(disabled=True)

    class Meta:
        model = Entrega
        fields = '__all__' 
        widgets = {
            'obs': forms.Textarea(attrs={'rows':3, 'cols':6}),
            'obs_nf': forms.Textarea(attrs={'rows':3, 'cols':6}),
            'cliente': autocomplete.ModelSelect2(
                url='cadastro:nome-autocomplete',
                attrs={'data-minimum-input-length': 3,},
                ),
            'transportadora': autocomplete.ModelSelect2(
                url='cadastro:transportadora-autocomplete',
                attrs={'data-minimum-input-length': 3,},
                ),
        }

class EntregaRetornoForm(forms.ModelForm):
    class Meta:
        model = NFe_transmissao
        fields = '__all__' 
        widgets = {
          'log': forms.Textarea(attrs={'rows':5, 'cols':8}),
          #'nfe': forms.Textarea(attrs={'rows':3, 'cols':6}),
          
        }

class Entrega_itens_BaseFormSet(BaseFormSet):
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
                pr_unit = Decimal(form.cleaned_data.get('pr_unit'))
                if pr_unit < 0:
                    print('erro pr_unit < 0')
                    raise forms.ValidationError(
                        'O preço deve maior ou igual a zero.',
                        code='valor_invalido')
            else:
                raise forms.ValidationError(
                    'O preço deve ser um valor numérico.',
                    code='valor_invalido')
            ncm = form.cleaned_data.get('ncm')

class Entrega_itens_formset(forms.Form):
    
    item_id = forms.CharField(max_length=30, label='Código', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '3'}))
    pedido = forms.CharField(max_length=30, label='Pedido', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '5'}))
    oc_cliente = forms.CharField(max_length=30, label='Código', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '5'}))
    cod = forms.CharField(max_length=30, label='Código', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '5'}))
    desc = forms.CharField(max_length=60, label='Descrição', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '50'}))
    unid = forms.CharField(max_length=6, label='Unidade', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '2'}))
    qtd = forms.CharField(max_length=15, label='Quantidade', required=False, widget=forms.TextInput(attrs={'size': '5'}))
    pr_unit = forms.CharField(max_length=15, label='Preço Unitário', required=False, widget=forms.TextInput(attrs={'size': '5'}))
    pr_tot = forms.CharField(max_length=15, label='Preço Total', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '6'}))
    obs = forms.CharField(max_length=500, label='Qtd. Entregue', required=False, disabled=True, widget=forms.TextInput(attrs={'size': '10'}))
    ncm = forms.CharField(max_length=500, label='Qtd. Entregue', required=False, disabled=False, widget=forms.TextInput(attrs={'size': '6'}))

