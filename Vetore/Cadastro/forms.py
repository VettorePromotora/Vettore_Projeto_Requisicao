from django import forms
from .models import Solicitacao, Status, Dados, Produtos
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UsuarioForm(UserCreationForm):
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.helper = FormHelper(UsuarioForm)
        #     self.helper.layout = Layout(Fieldset(
        #                                             Div('username', css_class="form-control"),
        #                                             Div('email', css_class="form-control"),
        #                                             Div('password1', css_class="form-control"),
        #                                             Div('password2', css_class="form-control"),
        #                                             Submit('submit', 'Submit', css_class='button white'),
        #                                         )
        #                                 )


