from django.forms import ModelForm
from .models import Produtos


class PostForm(ModelForm):
    class Meta:
        model = Produtos
        fields = {'status'}





