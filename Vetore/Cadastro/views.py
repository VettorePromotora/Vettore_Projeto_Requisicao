from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Local, Produtos, Categoria, Dados, Solicitacao
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.shortcuts import get_object_or_404

""" Implementando classes para o método de CREATE """


class CategoriaCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u"Matriz"
    model = Categoria
    fields = ['nome']
    template_name = 'Cadastro/formulario.html'
    success_url = reverse_lazy('listar-categoria')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Cadastro de categoria'
        context['botao'] = 'Cadastrar'
        return context


class LocalCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz"]
    model = Local
    fields = ['nome', 'descricao']
    template_name = 'Cadastro/formulario.html'
    success_url = reverse_lazy('listar-local')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Cadastro de local'
        context['botao'] = 'Cadastrar'
        return context


class ProdutosCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = [u"Matrix", u"Filial"]
    model = Produtos
    fields = ['cod_produto', 'nome', 'est_inic', 'est_min', 'categoria_f_m', 'unid_medida', 'descricao']
    template_name = 'Cadastro/formulario.html'
    success_url = reverse_lazy('listar-produtos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Cadastro de produto'
        context['botao'] = 'Cadastrar'
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
        return url


class DadosCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz"]
    model = Dados
    fields = ['arquivo']
    template_name = 'Cadastro/formulario-upload.html'
    success_url = reverse_lazy('listar-dados')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
        return url

    # def get_object(self, queryset=None):
    #     self.object = get_object_or_404(
    #         Dados, pk=self.kwargs['pk'], usuario=self.request.user
    #     )
    #     return self.object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['botao'] = 'cadastrar'
        return context


class SolicitarCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz", u"Filial"]
    model = Solicitacao
    fields = ['quantidade_solicita', 'observacao_solicita',
              'produto_solicita', 'destino', 'categoria']
    template_name = 'Cadastro/formulario.html'
    success_url = reverse_lazy('listar-solicitacao')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Solicitação de materiais'
        context['botao'] = 'Solicitar'
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
        return url


""" Implementando classes para o método de UPDATE """


class DadosUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz"]
    model = Dados
    fields = ['arquivo']
    template_name = 'Cadastro/formulario-upload.html'
    success_url = reverse_lazy('listar-dados')

    def get_object(self, queryset=None):
        self.object = get_object_or_404(Dados, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['botao'] = 'Salvar'
        return context


class CategoriaUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz"]
    model = Categoria
    fields = ['nome']
    template_name = 'Cadastro/formulario.html'
    success_url = reverse_lazy('listar-categoria')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Atualizar categoria'
        context['botao'] = 'Salvar'
        return context


class LocalUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz"]
    model = Local
    fields = ['nome', 'descricao']
    template_name = 'Cadastro/formulario.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Atualizar local'
        context['botao'] = 'Salvar'
        return context


class ProdutosUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz"]
    model = Produtos
    fields = ['cod_produto', 'nome', 'est_inic', 'est_min', 'descricao', 'unid_medida', 'categoria_f_m']
    template_name = 'Cadastro/formulario.html'
    success_url = reverse_lazy('listar-produtos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Atualizar produto'
        context['botao'] = 'Salvar'
        return context


class SolicitacaoUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz", u"Filial"]
    model = Solicitacao
    fields = ['quantidade_solicita', 'observacao_solicita',
              'produto_solicita', 'destino', 'categoria']
    template_name = 'Cadastro/formulario.html'
    success_url = reverse_lazy('listar-solicitacao')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Solicitação de materiais'
        context['botao'] = 'Salvar'


""" Implementando classes para o método de DELETE """


class DadosDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz"]
    template_name = 'Cadastro/Exclusao.html'
    success_url = reverse_lazy('listar-Dados')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Excluir arquivo'
        return context


class CategoriaDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz"]
    template_name = 'Cadastro/Exclusao.html'
    success_url = reverse_lazy('listar-categoria')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Excluir categoria'
        return context


class LocalDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz"]
    template_name = 'Cadastro/Exclusao.html'
    success_url = reverse_lazy('listar-local')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Excluir local'
        return context


class ProdutosDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz"]
    model = Produtos
    template_name = 'Cadastro/Exclusao.html'
    success_url = reverse_lazy('listar-produtos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Excluir produto'
        return context


class SolicitacaoDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz", u"Filial"]
    model = Solicitacao
    template_name = 'Cadastro/Exclusao.html'
    success_url = reverse_lazy('listar-solicitacao')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Excluir arquivo'
        return context


""" Implementando classes para o método de LIST """


class DadosList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz"]
    model = Categoria
    template_name = 'Cadastro/Listas/Dados' \
                    '.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Listar arquivos'
        return context


class CategoriaList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz", u"Filial"]
    model = Categoria
    template_name = 'Cadastro/Listas/categoria.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Listar Categorias'
        return context


class LocalList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz", u"Filial"]
    model = Local
    template_name = 'Cadastro/Listas/Local.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Listar locais'
        return context


class ProdutosList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz", u"Filial"]
    model = Produtos
    template_name = 'Cadastro/Listas/Produtos.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Listar produtos'
        return context

    # def get_queryset(self):
    #     self.object_list = Produtos.objects.filter(usuario=self.request.user)
    #     return self.object_list


class SolicitacaoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Matriz", u"Filial"]
    model = Solicitacao
    template_name = 'Cadastro/Listas/Solicitacao.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Listar solicitações'
        return context
