import random
from datetime import date

from django.db import models
from django.contrib.auth.models import User


def user_path(instance, filename):
    return 'usuario_{0}{1}'.format(instance.user.id, filename)


class Categoria(models.Model):
    """ Cadastro de Categorias """
    nome_categoria = models.CharField(max_length=100, default='-', unique=True)

    class Meta:
        ordering = ('nome_categoria',)

    def form_valid(self, form):
        form.instance.usuario = self.request.user  # models.ForeignKey(User, on_delete=models.PROTECT)
        url = super(Categoria, self).form_valid(form)
        return url

    def __str__(self):
        return '{}'.format(self.nome_categoria)


class Local(models.Model):

    """ Cadastro de Local """
    nome = models.CharField(max_length=50, default=' ')

    def __str__(self):
        return format(self.nome)


class Produtos(models.Model):
    Medidas = (
        ('un', 'Unidade'),
        ('cm', 'Centimetros'),
        ('mm', 'Milimetros'),
        ('m', 'Metros')
    )

    """ Cadastro de Atividades """
    nome = models.CharField(verbose_name='Produto', max_length=50, default=' ')
    est_inic = models.IntegerField(verbose_name='Estoque Inicial', default=0)
    est_min = models.IntegerField(verbose_name='Estoque Mínimo', default=0)
    descricao = models.TextField(verbose_name='Descrição', max_length=150, blank=True, null=True)
    unid_medida = models.CharField(verbose_name='Unidade de Medida', choices=Medidas, max_length=2, null=True)
    cod_produto = models.CharField(verbose_name='CÓD', max_length=120, unique=True, default='-')
    estoque_atl = models.PositiveIntegerField(verbose_name='Estoque atual', blank=True, default=0)

    categoria_f_m = models.ForeignKey(Categoria, on_delete=models.PROTECT, verbose_name='Categoria')
    estoque_local = models.ForeignKey(Local, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return '{} de {} ({})'.format(self.nome, self.categoria_f_m.nome_categoria, self.descricao)

    def to_dict_json(self):
        return {
            'pk': self.pk,
            'produto': self.nome,
            'estoque': self.estoque_atl,
        }


class Status(models.Model):
    """
    Cadastro de status
     param: status_mov - tipo de movimentação (Entada/Saída)
            status_prod - tipo de status por produto (Ativo/Inativo)
     """
    status_mov = models.CharField(verbose_name='Entrada', max_length=20, default='')
    status_prod = models.CharField(verbose_name='Saída', max_length=20, default='')

    def __str__(self):
        return self.status_mov, self.status_prod


class Dados(models.Model):
    """ Upload de arquivos """
    arquivo = models.FileField(upload_to='pdf/')

    def __str__(self):
        return 'nome: {}'.format(self.arquivo)


class Solicitacao(models.Model):
    status = models.CharField(verbose_name="Status", max_length=11, default="Pendente",)
    quantidade_solicita = models.IntegerField(verbose_name="Quantidade", null=True, default=0)
    observacao_solicita = models.TextField(verbose_name="Obs", null=True)
    data = models.DateField(auto_now=True)

    #  ForeingKeys
    produto_solicita = models.ForeignKey(Produtos, on_delete=models.CASCADE, verbose_name='Produto', null=True)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    destino = models.ForeignKey(Local, on_delete=models.PROTECT, verbose_name='Destino', null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, verbose_name='Categoria', null=True)

    class Meta:
        ordering = ('-data',)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super(Solicitacao, self).form_valid(form)
        return url

    def __str__(self):
        return '{} {} de {} para {} {} ({} {})'.format(self.quantidade_solicita, self.produto_solicita,
                                                       self.categoria, self.destino, self.observacao_solicita,
                                                       self.status, self.criado_por)


class Movimentacao(models.Model):
    """ Cadastro de Movimentações """
    tipo = models.ForeignKey(Status, on_delete=models.PROTECT)
    produto = models.ForeignKey(Produtos, on_delete=models.PROTECT)
    dt_movimetacao = models.DateField(verbose_name='Dt_Movimentação')
    locais = models.ForeignKey(Local, on_delete=models.PROTECT)
    categoria_f_m = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    def __str__(self):
        return '{}/ <span>{}</span> - {} <i>{}</i> ({} - {})'.format(self.locais.nome, self.tipo.status_mov,
                                                                     self.produto.nome, self.categoria_f_m.nome,
                                                                     self.produto.descricao, self.tipo.status_prod)


class Banco(models.Model):
    """ Cadastro de Bancos """
    vis = (('Compra de dívida', 'Compra de dívida'), ('Operações', 'Operações'), ('Ambos', 'Ambos'))
    visivel_app = (('Sim', 'Sim'), ('Não', 'Não'))
    visivel_corretor = (('Sim', 'Sim'), ('Não', 'Não'))
    pagar_bonus_comissao = (('Sim', 'Sim'), ('Não', 'Não'))

    codigo = models.IntegerField(verbose_name="Código", null=True, default=0)
    nome = models.CharField(max_length=50, default=' ')
    perc_encargos = models.IntegerField(verbose_name='Encargos Empresa (%)')
    visivel = models.CharField(verbose_name='Visível', choices=vis, max_length=16, null=True)
    perc_desconto_saldo_devedor = models.IntegerField(verbose_name='Saldo Devedor (%)')
    visualizar_app = models.CharField(verbose_name='visual. no App Cliente', choices=visivel_app, max_length=3, null=True)
    visivel_corretores = models.CharField(verbose_name='visível aos corretores', choices=visivel_corretor, max_length=3, null=True)
    pagar_bonus_junto_comissao = models.CharField(verbose_name='Pagar bônus com comissão', choices=pagar_bonus_comissao, max_length=3, null=True)
    responsavel = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    def __str__(self):
        return '{} - {}'.format(self.codigo, self.nome)


class ServicoBanco(models.Model):
    status_c = (
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo')
    )
    banco = models.ForeignKey(Banco, on_delete=models.PROTECT)
    produto = models.CharField(verbose_name='Produto', max_length=50, default=' ', null=True)

    def __str__(self):
        return '{}'.format(self.produto)


class GrupoComissao(models.Model):
    status_c = (
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo')
    )
    nome = models.CharField(max_length=50, default=' ')
    perc_comissao = models.IntegerField(verbose_name='Percentual')
    status_comissao = models.CharField(verbose_name='status', choices=status_c, max_length=7, null=True)
    observacao_comissao = models.TextField(verbose_name="Observações", null=True)

    def __str__(self):
        return '{}'.format(self.nome)

