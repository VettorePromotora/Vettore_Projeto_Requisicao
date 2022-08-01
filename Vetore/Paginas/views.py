""" Fluxos de Paginas """
from django.views.generic import TemplateView


# Create your views here.
class IndexView(TemplateView):
    """ Rota para a página index """
    template_name = 'Paginas/index.html'


class SobreView(TemplateView):
    """ Rota para a página Sobre """
    template_name = 'Paginas/sobre.html'

