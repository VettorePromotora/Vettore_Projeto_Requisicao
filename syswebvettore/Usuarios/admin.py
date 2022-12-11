from django.contrib import admin
from .models import Perfil, Setor, Contato, LoginBanco

# admin.site.register(Perfil)


class ContatoInline(admin.TabularInline):
    model = Contato


class LoginBancoInline(admin.TabularInline):
    model = LoginBanco


@admin.register(Perfil)
class DepartamentoSetorAdmin(admin.ModelAdmin):
    inlines = (ContatoInline, LoginBancoInline)
