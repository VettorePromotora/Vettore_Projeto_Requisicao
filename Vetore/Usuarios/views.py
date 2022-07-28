from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from .forms import UsuarioForm
from django.urls import reverse_lazy

from .models import Perfil

""" Implementando classes para o método de CREATE """


class UsuarioCreate(CreateView):
    template_name = 'Cadastro/formulario.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        grupo = get_object_or_404(Group, name="Cliente")

        url = super(UsuarioCreate, self).form_valid(form)
        self.object.groups.add(grupo)
        self.object.save()

        Perfil.objects.create(usuario=self.object)

        return url

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Registro de novo usuário'
        context['botao'] = 'Cadastrar'

        return context


""" Implementando classes para o método de UPDATE """


class PerfilUpdate(UpdateView):
    template_name = 'Cadastro/formulario.html'
    model = Perfil
    fields = ['nome_completo', 'cpf', 'telefone']
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        self.object = get_object_or_404(Perfil, usuario=self.request.user)
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super(PerfilUpdate, self).get_context_data(*args, **kwargs)
        context['titulo'] = 'Meus dados pessoais'
        context['botao'] = 'Atualizar'

        return context


