from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms.widgets import CheckboxSelectMultiple
from django_cpf_cnpj.fields import CPFField, CNPJField
from .models import Parceiro, Tipo_parceiro, Municipio, Estado

class ParcForm(forms.ModelForm):
    #cnpj = CNPJField(masked=False)
    class Meta:
        model = Parceiro # Your User model
        fields = '__all__'
        widgets = {'cnpj2': forms.TextInput(attrs={'data-mask':"00.000.000/0000-00"})}

    def __init__(self, *args, **kwargs):
        super(ParcForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-6'
        self.helper.form_id = 'id-ParcForm'
        self.helper.form_method = 'post'
        self.fields['tipo'].widget = CheckboxSelectMultiple()
        self.fields['tipo'].queryset = Tipo_parceiro.objects.all()
        self.helper.add_input(Submit('submit', 'Submit'))
       #acrescimo dependent dropdownlist
        self.fields['municipio'].queryset = Municipio.objects.none()

        if 'estado' in self.data:
            try:
                estado = self.data.get('estado')
                self.fields['municipio'].queryset = Municipio.objects.filter(estado=estado).order_by('nome')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            pass
            #self.fields['municipio'].queryset = self.instance.country.city_set.order_by('name')


class SearchParcForm(forms.Form):

    nome = forms.CharField(
        label = "Nome/Razão Social",
        max_length = 80,
        required = False,
    )

    cnpj = forms.CharField(
        label = "CNPJ/CPF",
        required = False,
    )

    cpf_cnpj = forms.CharField(
        label = "CNPJ/CPF",
        required = False,
    )

    cidade = forms.CharField(
        label = "Cidade",
        max_length = 80,
        required = False,
    )

    estado = forms.CharField(
        label = "Estado",
        required = False,
    )

    ativo = forms.TypedChoiceField(
        label = "Mostrar Inativos",
        choices = (('nao', "Não"), ('sim', "Sim")),
        #coerce = lambda x: bool(int(x)),
        widget = forms.RadioSelect,
        initial = 'nao',
        required = False,
    )

    def __init__(self, *args, **kwargs):
        super(SearchParcForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal' #blueForms' #'in-line' #
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-6'
        self.helper.form_id = 'id-ParcForm'
        #self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        #self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))

    def clean_cnpj(self):
        data = self.cleaned_data['cnpj']
        #data = '02.799.169/0001-89'
        if len(data)<18:
            pass
            #data = '99999999999'
            #raise forms.ValidationError('Valor não é válido')
            #cleaned_data['cnpj']='123456789'
            #return cleaned_data
        return data



    #def clean(self):
        #pass
        #super(forms.Form, self).clean() #I would always do this for forms.
        #data = self.cleaned_data
        #data['nome'] = 'tec l'

        ##self.cleaned_data['cnpj'] = data
        #self.cleaned_data['nome'] = 'data'
        #return data
