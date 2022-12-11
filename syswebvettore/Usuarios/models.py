from django.db import models
from django.contrib.auth.models import User
from Cadastro.models import Banco, Categoria, GrupoComissao


class Perfil(models.Model):
    contratacao = (
        ('CLT', 'CLT'),
        ('Estagiário', 'Estagiário'),
        ('Prestador de Serviço (MEI)', 'Prestador de Serviço (MEI)'),
    )
    s_contrato = (
        ('Concluído', 'Concluído'),
        ('Pendente', 'Pendente'),
    )
    demissao = (
        ('Sem justa causa', 'Sem justa causa'),
        ('Com justa causa', 'Com justa causa'),
        ('Pedido de demissão', 'Pedido de demissão'),
        ('Acordo', 'Acordo'),
        ('consensual', 'consensual'),
    )

    # Perfil
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=50, null=True)
    nome_mae = models.CharField(max_length=30, verbose_name='Nome da Mãe', default='', blank=True, null=True)
    nome_pai = models.CharField(max_length=30, verbose_name='Nome da Pai', default='', blank=True, null=True)
    cpf = models.CharField(max_length=14, null=True, verbose_name='CPF')
    rg = models.CharField(max_length=14, null=True, verbose_name='RG')
    org_exped = models.CharField(max_length=16, null=True)
    data_nasc = models.DateField(blank=True, null=True)
    data_emiss = models.DateField(blank=True, null=True)
    email_p = models.EmailField(blank=True, null=True, verbose_name='Email Pessoal')

    # Endereço
    logradouro = models.CharField(max_length=45, default='')
    numero_casa = models.IntegerField(verbose_name='Número', default=0)
    complemento_casa = models.CharField(max_length=10, default='')
    bairro = models.CharField(max_length=30, default='')
    estado = models.CharField(max_length=30, default='')
    cidade = models.CharField(max_length=30, default='')
    cep = models.CharField(max_length=15, default='')

    # Regime de Contratação
    local = models.CharField(max_length=20, null=True)
    grupo_comissiao = models.CharField(max_length=20, null=True)
    dt_cadastro = models.DateField(verbose_name='Data de cadastro', blank=True, null=True)
    dt_termino_contrato = models.DateField(verbose_name='Termino de contrato', blank=True, null=True)


    # CLT
    dt_inicio = models.DateField(verbose_name='Dt. de Inicio', blank=True, null=True)
    dt_deligamento = models.DateField(verbose_name='Data de desligamento', blank=True, null=True)
    tipo_demissao = models.CharField(verbose_name='Tipo de Demissão', choices=demissao, max_length=18, blank=True, null=True)

    # Estagiário
    dt_inicio_est = models.DateField(verbose_name='Dt. de Inicio', blank=True, null=True)
    fase_1_est = models.DateField(verbose_name='1° fase', blank=True, null=True)
    fase_2_est = models.DateField(verbose_name='2° fase', blank=True, null=True)

    # Prestador de Serviço (MEI)
    status_contrato = models.CharField(verbose_name='Tipo', choices=s_contrato, max_length=11, blank=True, null=True)
    dt_inicio_serv = models.DateField(verbose_name='Dt. de Inicio', blank=True, null=True)
    dt_efetivacao = models.DateField(verbose_name='Dt. de Efetivação', blank=True, null=True)

    def __str__(self):
        return "{} - {} |({} {})".format(self.pk, self.nome_completo, self.usuario, self.local)


class Contato(models.Model):
    tipo = (
        ('Residencial', 'Residencial'),
        ('Comercial', 'Comercial'),
        ('Celular', 'Celular'),
        ('WhatsApp', 'WhatsApp'),
    )

    # Contato
    proprietario = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    email_p = models.EmailField(blank=True, null=True, verbose_name='E-mail pessoal')
    email_c = models.EmailField(blank=True, null=True, verbose_name='E-mail corporativo')
    tipo_contato = models.CharField(verbose_name='Tipo', choices=tipo, max_length=11, blank=True, null=True)
    telefone = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return self.proprietario, self.telefone


class Setor(models.Model):
    """ Cadastro de Categorias """
    # usuario_perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, default='-', unique=True)

    class Meta:
        ordering = ('nome',)

    def form_valid(self, form):
        form.instance.usuario = self.request.user  # models.ForeignKey(User, on_delete=models.PROTECT)
        url = super(Setor, self).form_valid(form)
        return url

    def __str__(self):
        return '{}'.format(self.nome)


class LoginBanco(models.Model):

    status_banco = (
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo')
    )

    # Contato
    usuario_perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    usuario_banco = models.CharField(verbose_name='Usuário', max_length=16, blank=True, null=True)
    senha_banco = models.CharField(verbose_name='Senha', max_length=16, blank=True, null=True)
    banco_l = models.ForeignKey(Banco, on_delete=models.CASCADE, verbose_name='Banco')
    status_b = models.CharField(verbose_name='Status', choices=status_banco, max_length=7, blank=True, null=True)
    perfil = models.ForeignKey(Setor, on_delete=models.CASCADE)

    def __str__(self):
        return '{} | {} ({})'.format(self.usuario_banco, self.banco_l, self.status_banco)
