from django import forms
from .models import Perfil
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, MultiField, Div
from django.forms import ModelForm


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


class PerfilForm(forms.ModelForm):
    required_css_class = 'riquired-field'
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))




