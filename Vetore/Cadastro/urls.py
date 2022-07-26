""" Modulo para cadastros """
from django.urls import path
from .views import LocalCreate, ProdutosCreate, CategoriaCreate, DadosCreate
from .views import LocalUpdate, ProdutosUpdate, CategoriaUpdate, DadosUpdate
from .views import LocalDelete, ProdutosDelete, CategoriaDelete, DadosDelete
from .views import LocalList, ProdutosList, CategoriaList, DadosList

urlpatterns = [
   path('cadastrar/categoria', CategoriaCreate.as_view(), name='cadastrar-categoria'),
   path('cadastrar/local', LocalCreate.as_view(), name='cadastrar-local'),
   path('cadastrar/produtos', ProdutosCreate.as_view(), name='cadastrar-produtos'),
   path('Cadastrar/dados', DadosCreate.as_view(), name='cadastrar-dados'),

   path('editar/categoria', CategoriaUpdate.as_view(), name='editar-categoria'),
   path('editar/local/<int:pk>', LocalUpdate.as_view(), name='editar-local'),
   path('editar/produtos/<int:pk>', ProdutosUpdate.as_view(), name='editar-produtos'),
   path('editar/dados', DadosUpdate.as_view(), name='editar-dados'),

   path('excluir/categoria', CategoriaDelete.as_view(), name='excluir-categoria'),
   path('excluir/local/<int:pk>', LocalDelete.as_view(), name='excluir-local'),
   path('excluir/produtos/<int:pk>', ProdutosDelete.as_view(), name='excluir-produtos'),
   path('editar/dados', DadosDelete.as_view(), name='editar-dados'),

   path('listar/categoria', CategoriaList.as_view(), name='listar-categoria'),
   path('listar/local/', LocalList.as_view(), name='listar-local'),
   path('listar/produtos/', ProdutosList.as_view(), name='listar-produtos'),
   path('listar/dados', DadosList.as_view(), name='listar-dados'),
   ]
