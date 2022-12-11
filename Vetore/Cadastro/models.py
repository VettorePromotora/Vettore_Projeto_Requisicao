from django.db import models
from django.contrib.auth.models import User


def user_path(instance, filename):
    return 'usuario_{0}{1}'.format(instance.user.id, filename)


class Categoria(models.Model):
    """ Cadastro de Categorias """
    nome = models.CharField(max_length=100, default='-', unique=True)

    def form_valid(self, form):
        form.instance.usuario = self.request.user  # models.ForeignKey(User, on_delete=models.PROTECT)
        url = super(Categoria, self).form_valid(form)
        return url

    def __str__(self):
        return '{}'.format(self.nome)


class Local(models.Model):
    """ Cadastro de Local """
    nome = models.CharField(max_length=50, default='-')
    descricao = models.CharField(max_length=50, verbose_name='Descrição', default='Filial-Sede')

    def __str__(self):
        return 'nome: {} ({})'.format(self.nome, self.descricao)


class Produtos(models.Model):
    Medidas = (
        ('un', 'Unidade'),
        ('cm', 'Centimetros'),
        ('mm', 'Milimetros'),
        ('m', 'Metros')
    )

    """ Cadastro de Atividades """
    nome = models.CharField(verbose_name='Produto', max_length=50, default='-')
    est_inic = models.IntegerField(verbose_name='Estoque Inicial', default=0)
    est_min = models.IntegerField(verbose_name='Estoque Mínimo', default=0)
    descricao = models.TextField(verbose_name='Descrição', max_length=150, blank=True, null=True)
    unid_medida = models.CharField(verbose_name='Unidade de Medida', choices=Medidas, max_length=2, null=True)
    cod_produto = models.CharField(verbose_name='CÓD', max_length=120, unique=True, default='-')

    categoria_f_m = models.ForeignKey(Categoria, on_delete=models.PROTECT, verbose_name='Categoria')

    def __str__(self):
        return '{} de {} ({})'.format(self.nome, self.categoria_f_m.nome, self.descricao)


class Status(models.Model):
    """ Cadastro de status
     param: status_mov - tipo de movimentação (Entada/Saída)
            status_prod - tipo de status por produto (Ativo/Inativo)
     """
    status_mov = models.CharField(verbose_name='Entrada', max_length=20, default='')
    status_prod = models.CharField(verbose_name='Saída', max_length=20, default='')

    def __str__(self):
        return self.status_mov, self.status_prod


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


class Dados(models.Model):
    """ Upload de arquivos """
    arquivo = models.FileField(upload_to='pdf/')

    def __str__(self):
        return 'nome: {}'.format(self.arquivo)


class Solicitacao(models.Model):
    status = models.CharField(verbose_name="Status", max_length=11, default="Pendente",)
    quantidade_solicita = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Quantidade", null=True)
    observacao_solicita = models.TextField(verbose_name="Obs", null=True)

    #  ForeingKeys
    produto_solicita = models.ForeignKey(Produtos, on_delete=models.PROTECT, verbose_name='Produto', null=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    destino = models.ForeignKey(Local, on_delete=models.PROTECT, verbose_name='Destino', null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, verbose_name='Categoria', null=True)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super(Solicitacao, self).form_valid(form)
        return url

    def __str__(self):
        return '{} {} de {} para {} {} ({} {})'.format(self.quantidade_solicita, self.produto_solicita, self.categoria,
                                                    self.destino, self.observacao_solicita, self.status, self.criado_por)
