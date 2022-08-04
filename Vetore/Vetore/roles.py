from rolepermissions.roles import AbstractUserRole


class AdministradorDaPlataforma(AbstractUserRole):
    available_permissions = {'aceitar_requisicao': True, 'negar_requisicao': False}


class UsuariosDaPlataforma(AbstractUserRole):
    available_permissions = {'editar_requisicao': True, 'excluir_requisicao': False}
