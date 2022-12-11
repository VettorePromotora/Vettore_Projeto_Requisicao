import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from Cadastro.models import Local, GrupoComissao
from django.forms import inlineformset_factory, NumberInput, DateInput
from Usuarios.models import Contato, Perfil, LoginBanco, Setor


class UsuarioForm(UserCreationForm):
    tipo = (
        ('Residencial', 'Residencial'),
        ('Comercial', 'Comercial'),
        ('Celular', 'Celular'),
        ('WhatsApp', 'WhatsApp'),
    )

    contratacao = (
        ('CLT', 'CLT'),
        ('Estagiário', 'Estagiário'),
        ('Prestador de Serviço (MEI)', 'Prestador de Serviço (MEI)'),
    )

    s_contrato = (
        ('Concluído', 'Concluído'),
        ('Pendente', 'Pendente'),
    )

    demissao = (
        ('Sem justa causa', 'Sem justa causa'),
        ('Com justa causa', 'Com justa causa'),
        ('Pedido de demissão', 'Pedido de demissão'),
        ('Acordo', 'Acordo'),
        ('consensual', 'consensual'),
    )

    # Dados pessoais
    nome_completo = forms.CharField(max_length=150)
    nome_mae = forms.CharField(max_length=150, label='Nome do Mãe', required=False)
    nome_pai = forms.CharField(max_length=150, label='Nome do Pai', required=False)
    cpf = forms.CharField(max_length=15, label='CPF')
    rg = forms.CharField(max_length=15, label='RG')
    org_exped = forms.CharField(max_length=15, label='Org. Exp')
    data_nasc = forms.DateField(label="Dt. de Nascimento", required=True, widget=DateInput(format='%d/%m/%y', attrs={'type': 'date'}))
    data_emiss = forms.DateField(label="Data de Emissão", required=True, widget=DateInput(format='%d/%m/%y', attrs={'type': 'date'}))

    # Endereço
    logradouro = forms.CharField(max_length=50)
    numero_casa = forms.IntegerField(max_value=9999, min_value=0, label='Número', required=False)
    complemento_casa = forms.CharField(max_length=10, label='Complemento', required=False)
    estado = forms.CharField(max_length=30)
    bairro = forms.CharField(max_length=30)
    cidade = forms.CharField(max_length=30)
    cep = forms.CharField(max_length=15)

    # Contato
    telefone = forms.CharField(max_length=16)
    email_p = forms.EmailField(max_length=100, label='E-mail pessoal')
    email_c = forms.EmailField(max_length=100, label='E-mail corporativo')
    tipo_contato = forms.ChoiceField(choices=tipo)

    # Regime de Contratação
    dt_cadastro = forms.DateField(label='Dt. de Cadastro', disabled=True, required=False, widget=DateInput(attrs={'type':'date', 'value': datetime.date.today()}))
    termino_contrato = forms.DateField(label='Termino de contrato', required=False, widget=DateInput(attrs={'type': 'date'}))

    # CLT
    dt_inicio = forms.DateField(label='Dt. de Inicio', required=False, widget=DateInput(format='%d/%m/%y', attrs={'type': 'date'}))
    dt_deligamento = forms.DateField(label='Data de desligamento', required=False, widget=DateInput(format='%d/%m/%y', attrs={'type': 'date'}))
    tipo_demissao = forms.ChoiceField(choices=demissao)

    # Estagiário
    dt_inicio_est = forms.DateField(label='Dt. de Inicio', required=False, widget=DateInput(format='%d/%m/%y', attrs={'type': 'date'}))
    fase_1_est = forms.DateField(label='1° fase', required=False, widget=DateInput(format='%d/%m/%y', attrs={'type': 'date'}))
    fase_2_est = forms.DateField(label='2° fase', required=False, widget=DateInput(format='%d/%m/%y', attrs={'type': 'date'}))

    # Prestador de Serviço (MEI)
    status_contrato = forms.ChoiceField(choices=s_contrato)
    dt_inicio_serv = forms.DateField(label='Dt. de Inicio', required=False, widget=DateInput(format='%d/%m/%y', attrs={'type': 'date'}))
    dt_efetivacao = forms.DateField(label='Dt. de Efetivação', required=False, widget=DateInput(format='%d/%m/%y', attrs={'type': 'date'}))

    # ForeignKeys
    local = forms.ModelChoiceField(queryset=Local.objects.all())
    grupo = forms.ModelChoiceField(queryset=Group.objects.all(), label='Função')
    Login_banc = forms.ModelChoiceField(queryset=LoginBanco.objects.all())
    grupo_comissiao = forms.ModelChoiceField(queryset=GrupoComissao.objects.all())

    class Meta:
        model = User
        fields = ['username',
                  'nome_completo',
                  'rg',
                  'data_emiss',
                  'org_exped',
                  'cpf',
                  'email',
                  'data_nasc',
                  'password1',
                  'password2',
                  'grupo',
                  ]


class ContatoForm(forms.ModelForm):

    class Meta:
        model = Contato
        fields = '__all__'


class LoginBancoForm(forms.ModelForm):

    class Meta:
        model = LoginBanco
        fields = '__all__'


usuarioformset = inlineformset_factory(Perfil, Contato, form=ContatoForm, fields=('tipo_contato', 'telefone'), extra=1)
perfilformset = inlineformset_factory(Perfil, LoginBanco, form=LoginBancoForm, extra=1)

