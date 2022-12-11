from django import forms
from Cadastro.models import Produtos, Local
from Usuarios.models import Perfil, User

from .models import Estoque, EstoqueItens


class EstoqueForm(forms.ModelForm):

    class Meta:
        model = Estoque
        fields = '__all__'  # ('nf',)


class EstoqueItensEntradaForm(forms.ModelForm):

    class Meta:
        model = EstoqueItens
        fields = ['local', 'estoque', 'produto', 'quantidade', 'obs_estoque', 'saldo']

    def __init__(self, *args, **kwargs):
        super(EstoqueItensEntradaForm, self).__init__(*args, **kwargs)


class EstoqueItensSaidaForm(forms.ModelForm):

    class Meta:
        model = EstoqueItens
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EstoqueItensSaidaForm, self).__init__(*args, **kwargs)

        # Retorna somente produtos com estoque maior do que zero.
        self.fields['produto'].queryset = Produtos.objects.filter(estoque_atl__gt=0)
