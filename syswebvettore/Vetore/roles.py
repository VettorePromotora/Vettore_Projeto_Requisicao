from rolepermissions.roles import AbstractUserRole


class Administrador(AbstractUserRole):
    available_permissions = {
        'aceitar_requisicao': True,
        'negar_requisicao': True,
        'ver_requisicao': True,
        'excluir_requisicao': True,
        'criar_requisicao': True,

        'ver_usuarios': True,
        'excluir_usuarios': True,
        'editar_usuarios': True,

        'ver_estoque': True,
        'editar_estoque': True,
        'excluir_estoque': True,
        'criar_estoque': True,

        'ver_produtos': True,
        'editar_produtos': True,
        'excluir_produtos': True,
        'adicionar_produtos': True,

        'ver_categoria': True,
        'editar_categoria': True,
        'excluir_categoria': True,
        'criar_categoria': True,
    }


class Filial(AbstractUserRole):
    available_permissions = {
        'aceitar_requisicao': False,
        'negar_requisicao': False,
        'ver_requisicao': True,
        'excluir_requisicao': False,
        'criar_requisicao': True,

        'ver_usuarios': False,
        'excluir_usuarios': False,
        'editar_usuarios': False,

        'ver_estoque': True,
        'editar_estoque': True,
        'excluir_estoque': True,
        'criar_estoque': True,

        'ver_produtos': True,
        'editar_produtos': True,
        'excluir_produtos': True,
        'adicionar_produtos': True,

        'ver_categoria': True,
        'editar_categoria': False,
        'excluir_categoria': False,
        'criar_categoria': False,
    }
