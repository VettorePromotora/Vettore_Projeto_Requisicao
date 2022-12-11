from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import PerfilUpdate, PerfilList, PerfilCreate, PerfilUpdateAdm, UsuarioCreate
from Usuarios import views as v

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='Usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # path('registrar/', UsuarioCreate.as_view(), name='registrar'),
    path('registrar/', v.inserir, name='registrar'),

    path('criar-perfil/<int:pk>', PerfilCreate.as_view(), name='criar-perfil'),

    path('atualizar-dados/<int:pk>', PerfilUpdate.as_view(), name='atualizar-dados'),

    path('atualizar-dados-adm/<int:pk>', PerfilUpdateAdm.as_view(), name='atualizar-dados-adm'),

    path('usuario/<int:pk>', PerfilUpdate.as_view(), name='usuario'),

    path('excluir/usuario/<int:pk>', PerfilUpdate.as_view(), name='excluir-usuario'),

    path('listar/usuarios/', PerfilList.as_view(), name='listar-usuario'),

    ]
