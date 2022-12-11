""" Página para criar registros no Django """
from django.contrib import admin
from .models import Local, Produtos, Categoria, Movimentacao, Status, Dados, Solicitacao, GrupoComissao, Banco, \
    ServicoBanco
from Usuarios.models import Setor


class SolicitacaoCriadaPor(admin.ModelAdmin):
    readonly_fields = ('criado_por', )

    def save_model(self, request, obj, form, change):
        usuario = request.user
        obj.criado_por = usuario
        super(SolicitacaoCriadaPor, self).save_model(request, obj, form, change)
        return obj

    # def get_queryset(self, request):
    #     qs = super(SolicitacaoCriadaPor, self).get_queryset(request)
    #     qs = qs.filter(criado_por=request.user.groups.name)
    #     return qs


# Register your models here.
admin.site.register(Local)  # Cadastro de SEDE/FILIAL
admin.site.register(Produtos)  # cadastro de produtos
# admin.site.register(Categoria)  # Cadastro de categorias (limpeza, escritório, TI...)
# admin.site.register(Banco)  # Cadastro de entrada e saída de produtos
admin.site.register(Movimentacao)  # Cadastro de entrada e saída de produtos
admin.site.register(Status)
admin.site.register(Dados)
admin.site.register(GrupoComissao)
admin.site.register(Solicitacao, SolicitacaoCriadaPor)


class Departamento(admin.TabularInline):
    model = Setor


class BancoInline(admin.TabularInline):
    model = ServicoBanco



@admin.register(Categoria)
class DepartamentoSetorAdmin(admin.ModelAdmin):
    inlines = (Departamento,)


@admin.register(Banco)
class ServicoBancoAdmin(admin.ModelAdmin):
    inlines = (BancoInline,)


