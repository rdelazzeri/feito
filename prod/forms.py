from django import forms
from .models import *
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *

class CollectionForm(forms.ModelForm):

    class Meta:
        model = Prod
        exclude = ['ipi_Venda', ]

    def __init__(self, *args, **kwargs):
        super(CollectionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('cod'),
                Field('desc'),
                Fieldset('Composicao',
                    Formset('codComp')),
                Field('obs'),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
                )
            )






class ProdCompForm(forms.ModelForm):

    class Meta:
        model = ProdComp
        exclude = ()

ProdCompFormSet = inlineformset_factory(
    Prod, ProdComp, form=ProdCompForm,
    fields=['codProd', 'CodComp', 'qtd'], extra=1, can_delete=True
    )