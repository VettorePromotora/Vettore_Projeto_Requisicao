""" Página para criar registros no Django """
from django.contrib import admin
from .models import Local, Produtos, Categoria, Movimentacao, Status, Dados, Solicitacao

# Register your models here.
admin.site.register(Local)  # Cadastro de SEDE/FILIAL
admin.site.register(Produtos)  # cadastro de produtos
admin.site.register(Categoria)  # Cadastro de categorias (limpeza, escritório, TI...)
admin.site.register(Movimentacao)  # Cadastro de entrada e saída de produtos
admin.site.register(Status)
admin.site.register(Dados)
admin.site.register(Solicitacao)


