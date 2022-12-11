from datetime import datetime

from braces.views import GroupRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404, render, redirect

import Usuarios
from .forms import UsuarioForm, usuarioformset, perfilformset, ContatoForm, LoginBancoForm
from django.urls import reverse_lazy, reverse
from .models import Perfil, Contato, LoginBanco

""" Implementando classes para o método de CREATE """


class UsuarioCreate(GroupRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'Cadastro/formulario_usuario.html'
    group_required = u"Adminstrador"
    form_class = UsuarioForm
    success_url = reverse_lazy('listar-usuario')
    success_message = "Cadastrado com sucesso"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registro de novo usuário'
        context['botao'] = 'Cadastrar'
        if self.request.POST:
            context['form'] = UsuarioForm(self.request.POST)
            context['contato_form'] = usuarioformset(self.request.POST)
            context['perfil_form'] = perfilformset(self.request.POST)
        else:
            context['form'] = UsuarioForm()
            context['contato_form'] = usuarioformset()
            context['perfil_form'] = perfilformset()
        return context

    def form_valid(self, form):
        group = self.request.POST.get('grupo')
        grupo = get_object_or_404(Group, id=group)
        self.object.groups.add(grupo)
        self.object.save()

        Perfil.objects.create(
            usuario=self.object,
            nome_completo=self.request.POST.get('nome_completo'),
            cpf=self.request.POST.get('cpf'),
            rg=self.request.POST.get('rg'),
            org_exp=self.request.POST.get('org_exped'),
            telefone=self.request.POST.get('telefone'),
            local=self.request.POST.get('local'),
            data_nascimento=self.request.POST.get('data_nasc'),
            data_emissao=self.request.POST.get('data_emiss'),
            nome_mae=self.request.POST.get('nome_mae'),
            nome_pai=self.request.POST.get('nome_pai'),
            tipo_contato=self.request.POST.get('tipo_contato'),
            numero_casa=self.request.POST.get('numero_casa'),
            Estado=self.request.POST.get('estado'),
            Cidade=self.request.POST.get('cidade'),
            Bairro=self.request.POST.get('bairro'),
            complemento=self.request.POST.get('complemento_casa'),
            dt_cadastro=self.request.POST.get('dt_cadastro'),
            dt_inicio=self.request.POST.get('dt_inicio'),
            email_p=self.request.POST.get('email_p'),
            email_c=self.request.POST.get('email_c'),
        )

        context = self.get_context_data()
        forms = context['form']
        formset = context['contato_form']
        formset1 = context['perfil_form']
        if forms.is_valid() and formset.is_valid() or formset1.is_valid():
            self.object = form.save()
            forms.instance = self.object
            formset.instance = self.object
            formset1.instance = self.object
            forms.save()
            formset.save()
            formset1.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))

        return super(UsuarioCreate, self).form_valid(form)


def inserir(request):
    if request.method == "GET":
        form = UsuarioForm()
        contato_form = inlineformset_factory(Perfil, Contato, form=ContatoForm, fields=('tipo_contato', 'telefone'), extra=1)
        perfil_form = inlineformset_factory(Perfil, LoginBanco, form=LoginBancoForm, extra=1)

        context = {
            'titulo': 'Registro de novo usuário',
            'botao': 'Cadastrar',
            'form': form,
            'contato_form': contato_form,
            'perfil_form': perfil_form,
        }
        return render(request, 'Cadastro/formulario_usuario.html', context)

    elif request.method == "POST":

        Perfil.objects.create(
            usuario=request.user,
            nome_completo=request.POST.get('nome_completo'),
            cpf=request.POST.get('cpf'),
            rg=request.POST.get('rg'),
            org_exped=request.POST.get('org_exped'),
            local=request.POST.get('local'),
            data_nasc=request.POST.get('data_nasc'),
            data_emiss=request.POST.get('data_emiss'),
            nome_mae=request.POST.get('nome_mae'),
            nome_pai=request.POST.get('nome_pai'),
            numero_casa=request.POST.get('numero_casa'),
            estado=request.POST.get('estado'),
            cidade=request.POST.get('cidade'),
            bairro=request.POST.get('bairro'),
            complemento_casa=request.POST.get('complemento_casa'),
            dt_cadastro=request.POST.get('dt_cadastro'),
            dt_inicio=request.POST.get('dt_inicio'),
            email_p=request.POST.get('email_p'),
            dt_inicio_est=request.POST.get('dt_inicio_est'),
            fase_1_est=request.POST.get('fase_1_est'),
            fase_2_est=request.POST.get('fase_2_est'),
            status_contrato=request.POST.get('status_contrato'),
            dt_inicio_serv=request.POST.get('dt_inicio_serv'),
            dt_efetivacao=request.POST.get('dt_efetivacao'),
        )
        print(Perfil.usuario)

        form = UsuarioForm(request.POST)
        contato_form_set = inlineformset_factory(Perfil, Contato, form=ContatoForm)
        perfil_form_set = inlineformset_factory(Perfil, LoginBanco, form=LoginBancoForm)
        contato_form = contato_form_set(request.POST)
        perfil_form = perfil_form_set(request.POST)

        if form.is_valid() and contato_form.is_valid() and perfil_form.isvalid():
            cliente = form.save()
            contato_form.instance = cliente
            perfil_form.instance = cliente
            contato_form.save()
            perfil_form.save()
            return redirect(reverse('listar-usuario'))
        else:
            context = {
                'titulo': 'Registro de novo usuário',
                'botao': 'Cadastrar',
                'form': form,
                'contato_form': contato_form,
                'perfil_form': perfil_form,
            }
            return render(request, 'Cadastro/formulario_usuario.html', context)


class PerfilCreate(CreateView):
    template_name = "Cadastro/formulario.html"
    model = Perfil
    fields = '__all__'
    success_url = reverse_lazy('listar-usuario')

    def get_object(self, queryset=None):
        self.object = get_object_or_404(Perfil, usuario=self.request.user)
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super(PerfilCreate, self).get_context_data(*args, **kwargs)
        context['titulo'] = 'Meus dados pessoais'
        context['botao'] = 'Salvar'

        return context


""" Implementando classes para o método de UPDATE """


class PerfilUpdateAdm(GroupRequiredMixin, UpdateView):
    group_required = u"Administrador"
    template_name = "Cadastro/formulario_usuario.html"
    model = Perfil
    fields = '__all__'
    success_url = reverse_lazy('listar-usuario')

    def get_context_data(self, *args, **kwargs):
        context = super(PerfilUpdateAdm, self).get_context_data(*args, **kwargs)
        context['titulo'] = 'ATUALIZAR PERFIL'
        context['botao'] = 'Atualizar'

        return context


class PerfilUpdate(GroupRequiredMixin, UpdateView):
    group_required = u"Filial"
    template_name = "Cadastro/formulario_usuario_edit.html"
    model = Perfil
    fields = '__all__'
    success_url = reverse_lazy('listar-usuario')

    def get_context_data(self, *args, **kwargs):
        context = super(PerfilUpdate, self).get_context_data(*args, **kwargs)
        context['titulo'] = 'Meus dados pessoais'
        context['botao'] = 'Atualizar'

        return context


class PerfilList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz", u"Filial"]
    model = Usuarios
    template_name = 'Usuarios/Listas/Usuarios.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Usuários'
        return context

    def get_queryset(self):
        pesquisa = self.request.GET.get('search')

        if pesquisa:
            qtd = Perfil.objects.filter(nome_completo__icontains=pesquisa)
        else:
            qtd = Perfil.objects.all()

        return qtd


class PerfilDelete(DeleteView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz"]
    template_name = 'Cadastro/Exclusao.html'
    success_url = reverse_lazy('usuario')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Excluir usuario'
        return context


