from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import Produtos, Solicitacao, Categoria, Banco, ServicoBanco
from Usuarios.models import Setor


class PostForm(forms.ModelForm):

    class Meta:
        model = Produtos
        fields = '__all__'


class SolicitaForm(ModelForm):
    class Meta:
        model = Solicitacao
        fields = '__all__'


class CategoriaForm(forms.ModelForm):
    class Meta:
        abstract = True
        model = Categoria
        fields = '__all__'


class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = '__all__'


class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = '__all__'


class ServicoForm(forms.ModelForm):
    class Meta:
        model = ServicoBanco
        fields = '__all__'


departamentoform = inlineformset_factory(Categoria, Setor, form=CategoriaForm, extra=1)
