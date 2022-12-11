""" Fluxos de Paginas """
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from Cadastro.models import Local


class IndexView(ListView):
    """ Rota para a página index """
    login_url = reverse_lazy('login')
    group_required = [u"Administrador", u"Filial"]
    model = Local
    template_name = 'paginas/index.html'


class SobreView(TemplateView):
    """ Rota para a página Sobre """
    template_name = 'Paginas/sobre.html'


