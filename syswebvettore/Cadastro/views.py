import csv
import io
import os
from datetime import datetime
from django.db import utils
from django.forms import formset_factory, inlineformset_factory, modelformset_factory
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from estoque.models import EstoqueItens, EstoqueSaida
from .Import_Export.export_excel import export_xlsx
from .forms import PostForm, CategoriaForm, departamentoform, SetorForm, BancoForm, ServicoForm
from .models import Local, Produtos, Categoria, Dados, Solicitacao, Banco, GrupoComissao, ServicoBanco
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from braces.views import GroupRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from Usuarios.models import Perfil, Setor
from django.views.generic.detail import SingleObjectMixin

""" Implementando classes para o método de CREATE """

#
# class CategoriaCreate(GroupRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     template_name = 'Cadastro/formulario_departamento.html'
#     group_required = u"Administrador"
#     model = Categoria
#     form_setor = inlineformset_factory(Categoria, Setor, form=SetorForm, extra=1)
#     fields = '__all__'
#     success_url = reverse_lazy('listar-categoria')
#     success_message = "Departamento criado com sucesso!"
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(CategoriaCreate, self).get_context_data(**kwargs)
#         context['titulo'] = 'Cadastro de categoria'
#         context['botao'] = 'Cadastrar'
#         context['form_setor'] = self.form_setor
#         return context
#
#     def form_valid(self, form):
#         self.form_setor.intance = form
#
#         url = super(CategoriaCreate, self).form_valid(form)
#         return url


def departamento_add(request):
    if request.method == 'GET':
        form = CategoriaForm()
        form_setor_factory = inlineformset_factory(Categoria, Setor, form=CategoriaForm)
        form_setor = form_setor_factory()
        context = {
            'titulo': 'Cadastro de categoria',
            'botao': 'Cadastrar',
            'form': form,
            'form_setor': form_setor,
        }
        return render(request, 'Cadastro/formulario_departamento.html', context)
    elif request.method == 'POST':
        form = CategoriaForm(request.POST)
        form_setor_factory = inlineformset_factory(Categoria, Setor, form=CategoriaForm)
        form_setor = form_setor_factory(request.POST)

        if form.is_valid() and form_setor.is_valid():
            departamento = form.save()
            form_setor.instance = departamento
            form_setor.save()
            success_message = "Departamento criado com sucesso!"
            return redirect(reverse('listar-categoria'))
        else:
            context = {
                'titulo': 'Cadastro de categoria',
                'botao': 'Cadastrar',
                'form': form,
                'form_setor': form_setor,
            }
            return render(request, 'Cadastro/formulario_departamento.html', context)


class LocalCreate(GroupRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador"]
    model = Local
    fields = ['nome']
    template_name = 'Cadastro/formulario.html'
    success_url = reverse_lazy('listar-local')
    success_message = "Local: criado com sucesso!"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Cadastro de local'
        context['botao'] = 'Cadastrar'
        return context


class ProdutosCreate(GroupRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador", u"Filial"]
    model = Produtos
    fields = ['cod_produto', 'nome', 'est_inic', 'est_min', 'descricao', 'unid_medida',
              'categoria_f_m', 'estoque_local']

    template_name = 'Cadastro/formulario_produto.html'
    success_url = reverse_lazy('listar-produtos')
    success_message = "Produto: criado com sucesso!"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Cadastro de produto'
        context['botao'] = 'Cadastrar'
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
        return url


class SolicitarCreate(GroupRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador", u"Filial"]
    model = Solicitacao
    fields = ['quantidade_solicita', 'observacao_solicita', 'produto_solicita', 'destino', 'categoria']
    template_name = 'Cadastro/formulario_solicitacao.html'
    success_url = reverse_lazy('listar-solicitacao')
    success_message = "Solicitação: criada com sucesso!"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Solicitação de materiais'
        context['botao'] = 'Solicitar'
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
        return url


class BancoCreate(GroupRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Banco
    fields = '__all__'
    form_servico_factory = inlineformset_factory(Banco, ServicoBanco, form=BancoForm)
    template_name = 'Cadastro/formulario_banco.html'
    success_url = reverse_lazy('index')
    success_message = "Banco cadastrado com sucesso!"

    def get_context_data(self, *args, **kwargs):
        context = super(BancoCreate, self).get_context_data(**kwargs)
        context['titulo'] = 'Cadastrar Banco'
        context['botao'] = 'Cadastrar'
        context['form_servico'] = self.form_servico_factory()
        return context

    def form_valid(self, form):
        forms = self.get_context_data()
        form = forms['form']
        form_servico_factory = forms['form_servico']
        form_servico = form_servico_factory

        if form.is_valid() and form_servico.is_valid():
            departamento = form.save()
            form_servico.instance = departamento
            form_servico.save()
            return redirect(reverse('index'))
        return super(BancoCreate, self).form_valid(form)


def banco_add(request):
    if request.method == 'GET':
        form = BancoForm()
        form_servico_factory = inlineformset_factory(Banco, ServicoBanco, form=BancoForm)
        form_servico = form_servico_factory()
        context = {
            'titulo': 'Cadastrar Banco',
            'botao': 'Cadastrar',
            'form': form,
            'form_servico': form_servico,
        }
        return render(request, 'Cadastro/formulario_banco.html', context)

    elif request.method == 'POST':
        form = BancoForm(request.POST)
        form_servico_factory = inlineformset_factory(Banco, ServicoBanco, form=BancoForm)
        form_servico = form_servico_factory(request.POST)

        if form.is_valid() and form_servico.is_valid():
            departamento = form.save()
            form_servico.instance = departamento
            form_servico.save()
            message = "Departamento criado com sucesso!"
            return redirect(reverse('index'), message=message)
        else:
            context = {
                'titulo': 'Cadastro Banco',
                'botao': 'Cadastrar',
                'form': form,
                'form_servico': form_servico,
            }
            return render(request, 'Cadastro/formulario_banco.html', context)


class GrupoComissaoCreate(GroupRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = GrupoComissao
    fields = '__all__'
    template_name = 'Cadastro/formulario_comissao.html'
    success_url = reverse_lazy('listar-comissao')
    success_message = "Grupo comissionado registrado com sucesso!"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Cadastrar Grupo Comissionado'
        context['botao'] = 'Cadastrar'
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
        return url


class DadosCreate(GroupRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador"]
    model = Dados
    fields = ['arquivo']
    template_name = 'Cadastro/formulario-upload.html'
    success_url = reverse_lazy('listar-produtos')
    success_message = "Dados importados com sucesso!"

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super().form_valid(form)

        pasta = os.listdir('uploads/pdf/')

        produtos = []
        with open('uploads/pdf/'+pasta[0], 'r') as csv_file:
            data = list(csv.reader(csv_file, delimiter=';'))
            for row in data[1:]:
                produtos.append(
                    Produtos(
                        nome=row[0],
                        est_inic=row[1],
                        est_min=row[2],
                        descricao=row[3],
                        unid_medida=row[4],
                        cod_produto=row[5],
                        categoria_f_m=Categoria.objects.get(nome=row[6]),
                        estoque_atl=row[7],
                        estoque_local=Local.objects.get(nome=row[8])

                    )
                )
        try:
            Produtos.objects.bulk_create(produtos)
        except Exception as exception:
            if isinstance(exception, utils.IntegrityError):
                message = 'Você esta tentando importar produtos que já foram cadastrados.'
                return message
        return url

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            Dados, pk=self.kwargs['pk'], usuario=self.request.user
        )
        return self.object


""" Implementando classes para o método de UPDATE """


class DadosUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador"]
    model = Dados
    fields = ['arquivo']
    template_name = 'Cadastro/formulario-upload.html'
    success_url = reverse_lazy('listar-dados')
    success_message = "Dados: Atualizados com sucesso!"

    def get_object(self, queryset=None):
        self.object = get_object_or_404(Dados, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['botao'] = 'Salvar'
        return context


class CategoriaUpdate(GroupRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador"]
    model = Categoria
    fields = ['nome']
    template_name = 'Cadastro/formulario.html'
    success_url = reverse_lazy('listar-categoria')
    success_message = "Categoria: Atualizada com sucesso!"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Atualizar categoria'
        context['botao'] = 'Salvar'
        return context


class LocalUpdate(GroupRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador"]
    model = Local
    fields = ['nome', 'descricao']
    template_name = 'Cadastro/formulario.html'
    success_url = reverse_lazy('index')
    success_message = "Local: Atualizado com sucesso!"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Atualizar local'
        context['botao'] = 'Salvar'
        return context


class ProdutosUpdate(GroupRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador"]
    model = Produtos
    fields = ['cod_produto', 'nome', 'est_inic', 'est_min', 'descricao', 'unid_medida', 'categoria_f_m']
    template_name = 'Cadastro/formulario.html'
    success_url = reverse_lazy('listar-produtos')
    success_message = "Produto: Atualizado com sucesso!"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = 'Atualizar produto'
        context['botao'] = 'Salvar'
        return context


class SolicitacaoUpdate(GroupRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador", u"Filial"]
    model = Solicitacao
    fields = ['quantidade_solicita', 'observacao_solicita', 'produto_solicita', 'destino', 'categoria']
    template_name = 'Cadastro/formulario.html'
    success_url = reverse_lazy('listar-solicitacao')
    success_message = "Solicitação: Atualizada com sucesso!"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Solicitação de materiais'
        context['botao'] = 'Salvar'
        return context


class SolicitacaoAdminUpdate(GroupRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador", u"Filial"]
    model = Solicitacao
    fields = ['quantidade_solicita', 'observacao_solicita', 'produto_solicita', 'destino', 'categoria']
    template_name = 'Cadastro/formulario.html'
    success_url = reverse_lazy('listar-solicitacaoadmin')
    success_message = "Solicitação: Atualizada com sucesso!"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Solicitação de materiais'
        context['botao'] = 'Salvar'
        return context


class AceitarSolicitacaoUpdate(GroupRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador"]
    model = Solicitacao
    fields = ['status']
    template_name = 'Cadastro/Listas/aceitarsolicitacao.html'
    success_url = reverse_lazy('listar-solicitacaoadmin')
    success_message = "Solicitação: Aceita com sucesso!"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Aceitar Solicitação'
        context['botao'] = 'Salvar'

        return context


class NegarSolicitacaoUpdate(GroupRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador"]
    model = Solicitacao
    fields = ['status']
    template_name = 'Cadastro/negar.html'
    success_url = reverse_lazy('listar-solicitacaoadmin')
    success_message = "Solicitação: Rejeitada com sucesso!"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Negar Solicitação'
        context['botao'] = 'Salvar'

        return context


class GrupoComissaoUpdate(GroupRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador"]
    model = GrupoComissao
    fields = '__all__'
    template_name = 'Cadastro/formulario_Comissao.html'
    success_url = reverse_lazy('editar-comissao')
    success_message = "Comissão atualizada com sucesso!"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = 'Grupos de Comissionamento'
        context['botao'] = 'Salvar'

        return context


""" Implementando classes para o método de DELETE """


class DadosDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador"]
    template_name = 'Cadastro/Exclusao.html'
    # success_url = reverse_lazy('listar-Dados')

    def get_success_url(self):
        messages.success(self.request, "Registro excluido com sucesso!")
        return reverse('listar-Dados')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Excluir arquivo'
        return context


class CategoriaDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador"]
    template_name = 'Cadastro/Exclusao.html'
    # success_url = reverse_lazy('listar-categoria')

    def get_success_url(self):
        messages.success(self.request, "Categoria excluida com sucesso!")
        return reverse('listar-categoria')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Excluir categoria'
        return context


class LocalDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador"]
    template_name = 'Cadastro/Exclusao.html'
    # success_url = reverse_lazy('listar-local')

    def get_success_url(self):
        messages.success(self.request, "Local excluido com sucesso!")
        return reverse('listar-local')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Excluir local'
        return context


class ProdutosDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador"]
    model = Produtos
    template_name = 'Cadastro/Exclusao.html'
    # success_url = reverse_lazy('listar-produtos')

    def get_success_url(self):
        messages.success(self.request, "Produto excluido com sucesso!")
        return reverse('listar-produtos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = 'Excluir produto'
        return context


class SolicitacaoDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador", u"Filial"]
    model = Solicitacao
    template_name = 'Cadastro/Exclusao.html'
    success_url = reverse_lazy('listar-solicitacao')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Excluir arquivo'
        return context


class GrupoComissaoDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador"]
    model = GrupoComissao
    template_name = 'Cadastro/Exclusao.html'
    # success_url = reverse_lazy('listar-comissao')

    def get_success_url(self):
        messages.success(self.request, "Produto excluido com sucesso!")
        return reverse('listar-comissao')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Excluir Grupo de Comissao'
        return context


""" Implementando classes para o método de LIST """


class DadosList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador"]
    model = Categoria
    template_name = 'Cadastro/Listas/Dados.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Listar arquivos'
        return context

    def get_queryset(self):
        pesquisa = self.request.GET.get('search')

        if pesquisa:
            qtd = Dados.objects.filter(quantidade_solicita__icontains=pesquisa)
        else:
            qtd = Dados.objects.all()

        return qtd


class CategoriaList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador", u"Filial"]
    model = Categoria
    template_name = 'Cadastro/Listas/categoria.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Listar Categorias'
        return context

    def get_queryset(self):
        pesquisa = self.request.GET.get('search')

        if pesquisa:
            qtd = Categoria.objects.filter(quantidade_solicita__icontains=pesquisa)
        else:
            qtd = Categoria.objects.all()

        return qtd


class LocalList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador", u"Filial"]
    model = Local
    template_name = 'Cadastro/Listas/Local.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Listar locais'
        return context

    def get_queryset(self):
        pesquisa = self.request.GET.get('search')

        if pesquisa:
            qtd = Local.objects.filter(quantidade_solicita__icontains=pesquisa)
        else:
            qtd = Local.objects.all()

        return qtd


class ProdutosList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador", u"Filial"]
    model = Produtos
    template_name = 'Cadastro/Listas/Produtos.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = 'Listar produtos'
        return context

    def get_queryset(self):

        usuario = self.request.user.pk
        usuario = Perfil.objects.filter(pk=usuario)
        usuario_grupo = self.request.user.groups.all()
        usuario_grupo = usuario_grupo[0]
        usuario_local = usuario[0].local

        # if str(usuario) == "Administrador":
        #     filtro = Produtos.objects.filter(estoque_local__id=1)
        #     return filtro

        if str(usuario_grupo) != "Administrador":

            filtro1 = Produtos.objects.filter(estoque_local__nome=usuario_local)
            return filtro1

        pesquisa = self.request.GET.get('search')
        if pesquisa:
            qtd = Produtos.objects.filter(nome__icontains=pesquisa)
            return qtd
        else:
            qtd = Produtos.objects.all()
            return qtd


class SolicitacaoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador", u"Filial"]
    model = Solicitacao
    template_name = 'Cadastro/Listas/Solicitacao.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Listar solicitações'
        return context

    def get_queryset(self):
        pesquisa = self.request.GET.get('search')

        if pesquisa:
            qtd = Solicitacao.objects.filter(produto_solicita__nome__icontains=pesquisa)
        else:
            qtd = Solicitacao.objects.all()

        return qtd


class SolicitacaoAdminList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador"]
    model = Solicitacao
    template_name = 'Cadastro/Listas/Solicitacao_admin.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'solicitações pendentes'
        return context

    def get_queryset(self):
        pesquisa = self.request.GET.get('search')

        if pesquisa:
            qtd = Solicitacao.objects.filter(quantidade_solicita__icontains=pesquisa)
        else:
            qtd = Solicitacao.objects.all()

        return qtd


class SolicitacaoAceitaList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador"]
    model = Solicitacao
    template_name = 'Cadastro/Listas/Solicitacao_aceita.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'solicitações aceitas'
        return context

    def get_queryset(self):
        pesquisa = self.request.GET.get('search')

        if pesquisa:
            qtd = Solicitacao.objects.filter(quantidade_solicita__icontains=pesquisa)
        else:
            qtd = Solicitacao.objects.all()

        return qtd


class GrupoComissaoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador"]
    model = GrupoComissao
    template_name = 'Cadastro/Listas/Grupo_Comissao.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Grupos de Comissionameno'
        return context

    def get_queryset(self):
        pesquisa = self.request.GET.get('search')

        if pesquisa:
            qtd = GrupoComissao.objects.filter(quantidade_solicita__icontains=pesquisa)
        else:
            qtd = GrupoComissao.objects.all()

        return qtd


def dando_baixa_estoque(request, pk):
    entrega = Solicitacao.objects.get(pk=pk)

    valor = entrega.produto_solicita.estoque_atl - entrega.quantidade_solicita
    if (valor > entrega.produto_solicita.estoque_atl) and (valor < 0):
        return messages.error(request, 'Estoque não disponível.')
    else:

        # criar um Estoque saida
        estoque_saida = EstoqueSaida.objects.create(
            funcionario=request.user,
            movimento='s'
        )

        if entrega.status == "Aceito":
            EstoqueItens.objects.create(
                estoque=estoque_saida,
                local=entrega.destino,  # novo 20/10/2022
                produto=entrega.produto_solicita,
                quantidade=entrega.quantidade_solicita,
                saldo=entrega.produto_solicita.estoque_atl - entrega.quantidade_solicita
            )

            v = Produtos.objects.get(pk=entrega.produto_solicita.pk)
            v.estoque_atl = valor
            v.save()

            # Dar baixa no estoque
            produtos = estoque_saida.estoques.all()
            for item_produto in produtos:
                produto = Produtos.objects.get(pk=item_produto.produto.pk)
                produto.estoque = item_produto.saldo
                produto.save()
    entrega.estoque_atualizado = True
    entrega.save()

    entrega.status = "Retirado"
    entrega.save()

    messages.success(request, 'Estoque atualizado com sucesso.')
    return HttpResponseRedirect(reverse_lazy('listar-solicitacaoaceita'))


############################################################################


def dar_baixa_estoque(form):
    # Pega os produtos a partir da instância do formulário (Estoque).
    Produtos = form.estoques.all()
    for item in Produtos:
        produto = Produtos.objects.get(pk=item.Produtos.pk)
        produto.estoque = item.saldo
        produto.save()
    print('Estoque atualizado com sucesso.')


def produto_detail(request, pk):
    template_name = 'produto_detail.html'
    obj = Produtos.objects.get(pk=pk)
    context = {'object': obj}
    return render(request, template_name, context)


def csv_to_list(filename: str) -> str:
    with open(filename) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        csv_data = [line for line in reader]
    return csv_data


def export_csv(request):

    produtos = Produtos.objects.all()

    options = Produtos._meta
    fields = [field.name for field in options.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'atachment; filename="produtos.csv"'

    writer = csv.writer(response)

    writer.writerow([options.get_field(field).verbose_name for field in fields])

    for obj in produtos:
        writer.writerow([getattr(obj, field) for field in fields])

    return response


def import_xlsx(request):
    filename = 'Cadastro/uploads/pdf/<slug:slug>.xlsx'
    import_xlsx(filename)
    messages.success(request, 'Produtos importados com sucesso.')
    return HttpResponseRedirect(reverse('produto:produto_list'))


def exportar_produtos_xlsx(request):
    MDATA = datetime.now().strftime('%Y-%m-%d')
    model = Produtos
    filename = 'Cadastro/uploads/pdf/<slug:slug>.xlsx'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{MDATA}.{_filename[1]}'
    queryset = Produtos.objects.all().values_list(
        'nome',
        'est_inic',
        'est_min',
        'descricao',
        'unid_medida',
        'cod_produto',
    )
    columns = ('nome', 'est_inic', 'est_min', 'descricao', 'unid_medida', 'cod_produto')
    response = export_xlsx(model, filename_final, queryset, columns)
    return response


from django.shortcuts import render


def notificacao(request, Solicitacao):
    x = Solicitacao.objects.filter(status="Pendente")

    return render(request, 'Paginas/paginas/index.html', {'Notificar': x})


def produto_json(request, pk):
    produto = Produtos.objects.filter(pk=pk)
    data = [item.to_dict_json() for item in produto]
    return JsonResponse({'data': data})


