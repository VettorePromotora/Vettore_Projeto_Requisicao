""" Módulo para cadastros """
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import LocalCreate, ProdutosCreate, DadosCreate, SolicitarCreate, NegarSolicitacaoUpdate, \
   BancoCreate, GrupoComissaoCreate, GrupoComissaoUpdate, GrupoComissaoDelete, GrupoComissaoList

from .views import LocalUpdate, ProdutosUpdate, CategoriaUpdate, DadosUpdate, SolicitacaoUpdate, SolicitacaoAdminUpdate, produto_json

from .views import LocalDelete, ProdutosDelete, CategoriaDelete, DadosDelete, SolicitacaoDelete

from .views import LocalList, ProdutosList, CategoriaList, DadosList, SolicitacaoList, SolicitacaoAdminList, \
   SolicitacaoAceitaList, AceitarSolicitacaoUpdate
from Cadastro import views as v


urlpatterns = [
   # path('cadastrar/categoria/', CategoriaCreate.as_view(), name='cadastrar-categoria'),
   path('cadastrar/categoria/', v.departamento_add, name='cadastrar-categoria'),
   path('cadastrar/local/', LocalCreate.as_view(), name='cadastrar-local'),
   path('cadastrar/produtos/', ProdutosCreate.as_view(), name='cadastrar-produtos'),
   path('Cadastrar/dados/', DadosCreate.as_view(), name='cadastrar-dados'),
   path('cadastrar/solicitacao/', SolicitarCreate.as_view(), name='cadastrar-solicitacao'),
   # path('cadastrar/banco/', BancoCreate.as_view(), name='cadastrar-banco'),
   path('cadastrar/banco/', v.banco_add, name='cadastrar-banco'),
   path('cadastrar/comissao/', GrupoComissaoCreate.as_view(), name='cadastrar-comissao'),

   path('editar/categoria/<int:pk>', CategoriaUpdate.as_view(), name='editar-categoria'),
   path('editar/local/<int:pk>', LocalUpdate.as_view(), name='editar-local'),
   path('editar/produtos/<int:pk>', ProdutosUpdate.as_view(), name='editar-produtos'),
   path('editar/dados/<int:pk>', DadosUpdate.as_view(), name='editar-dados'),
   path('editar/solicitacao/<int:pk>', SolicitacaoUpdate.as_view(), name='editar-solicitacao'),
   path('editar/solicitacaoadmin/<int:pk>', SolicitacaoAdminUpdate.as_view(), name='editar-solicitacaoadmin'),
   path('editar/comissao/<int:pk>', GrupoComissaoUpdate.as_view(), name='editar-comissao'),

   path('editar/aceitarsolicitacao/<int:pk>', AceitarSolicitacaoUpdate.as_view(), name='aceitar-solicitacao'),
   path('editar/negarsolicitacao/<int:pk>', NegarSolicitacaoUpdate.as_view(), name='negar-solicitacao'),

   path('excluir/categoria/<int:pk>', CategoriaDelete.as_view(), name='excluir-categoria'),
   path('excluir/local/<int:pk>', LocalDelete.as_view(), name='excluir-local'),
   path('excluir/produtos/<int:pk>', ProdutosDelete.as_view(), name='excluir-produtos'),
   path('excluir/dados/<int:pk>', DadosDelete.as_view(), name='excluir-dados'),
   path('excluir/solicitacao/<int:pk>', SolicitacaoDelete.as_view(), name='excluir-solicitacao'),
   path('excluir/comissao/<int:pk>', GrupoComissaoDelete.as_view(), name='excluir-comissao'),

   path('listar/categoria', CategoriaList.as_view(), name='listar-categoria'),
   path('listar/local/', LocalList.as_view(), name='listar-local'),
   path('listar/produtos/', ProdutosList.as_view(), name='listar-produtos'),
   path('listar/dados/', DadosList.as_view(), name='listar-dados'),
   path('listar/solicitacao/', SolicitacaoList.as_view(), name='listar-solicitacao'),
   path('listar/solicitacaoadmin/', SolicitacaoAdminList.as_view(), name='listar-solicitacaoadmin'),
   path('listar/solicitacaoaceita/', SolicitacaoAceitaList.as_view(), name='listar-solicitacaoaceita'),
   path('listar/comissao/', GrupoComissaoList.as_view(), name='listar-comissao'),

   path('dandobaixa/<int:pk>', v.dando_baixa_estoque, name='dando-baixa'),
   path('downloads/', v.export_csv, name='exportar-dados'),

   path('accounts/', include('django.contrib.auth.urls')),
   path('alterar-senha/', auth_views.PasswordChangeView.as_view(template_name='Cadastro/formulario_usuario.html')),
   path('editar/produtos/json/<int:pk>/', v.produto_json, name='produto_json'),
   ]

