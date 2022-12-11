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

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper(UsuarioForm)
            self.helper.layout = Layout(Fieldset(
                                                    Div('username', css_class="form-control"),
                                                    Div('email', css_class="form-control"),
                                                    Div('password1', css_class="form-control"),
                                                    Div('password2', css_class="form-control"),
                                                    Submit('submit', 'Submit', css_class='button white'),
                                                )
                                        )


# class CommentForm(forms.Form):
#     email = forms.EmailField(max_length=100)
#     username = forms.CharField()
#     password1 = forms.PasswordInput()
#     password2 = forms.PasswordInput()
#     usuario = forms.CharField()
#
#     username.widget.attrs.update({'class': 'form-control'})
#     email.widget.attrs.update({'class': 'form-control'})
#     usuario.widget.attrs.update({'class': 'form-control'})






