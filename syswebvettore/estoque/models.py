import random

from django.contrib.auth.models import User
from django.db import models

from django.urls import reverse_lazy

from Paginas.models import TimeStampedModel
from Cadastro.models import Produtos, Local
from smart_selects.db_fields import ChainedForeignKey

from .managers import EstoqueEntradaManager, EstoqueSaidaManager

MOVIMENTO = (
    ('e', 'entrada'),
    ('s', 'saida'),
)


class Estoque(TimeStampedModel):
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nf = models.PositiveIntegerField('nota fiscal', null=True, blank=True)
    movimento = models.CharField(max_length=1, choices=MOVIMENTO, blank=True)
    est_local = models.ForeignKey(Local, on_delete=models.CASCADE, blank=True, default=1)
    est_destino = models.ForeignKey(Local, on_delete=models.CASCADE, null=True, blank=True, default=2, related_name='destino_env')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        if self.nf:
            self.nf = random.randint(0, 1000)
            return '{} - {} - {}'.format(self.pk, self.nf, self.created.strftime('%d-%m-%Y'))
        return '{} --- {}'.format(self.pk, self.created.strftime('%d-%m-%Y'))

    def nf_formated(self):
        if self.nf:

            return str(self.nf).zfill(3)
        return '---'


class EstoqueEntrada(Estoque):

    objects = EstoqueEntradaManager()

    class Meta:
        proxy = True
        verbose_name = 'estoque entrada'
        verbose_name_plural = 'estoque entrada'


class EstoqueSaida(Estoque):

    objects = EstoqueSaidaManager()

    class Meta:
        proxy = True
        verbose_name = 'estoque saída'
        verbose_name_plural = 'estoque saída'


class EstoqueItens(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE, related_name='estoques')
    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE, related_name='estoques')
    produto = ChainedForeignKey(Produtos, chained_field="local", chained_model_field="estoque_local", auto_choose=True)
    quantidade = models.PositiveIntegerField()
    destino = models.ForeignKey(Local, on_delete=models.CASCADE, related_name='destino', null=True)
    obs_estoque = models.TextField(verbose_name='Observação', max_length=150, blank=True, null=True)
    saldo = models.PositiveIntegerField(blank=True)

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return '{} - {} - {}'.format(self.pk, self.estoque.pk, self.produto)


class ProtocoloEntrega(TimeStampedModel):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estoque_atualizado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse_lazy('estoque:protocolo_de_entrega_detail', kwargs={'pk': self.pk})


class ProtocoloEntregaItens(models.Model):
    protocolo_entrega = models.ForeignKey(
        ProtocoloEntrega,
        on_delete=models.CASCADE,
        related_name='protocolo_entrega'
    )
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return '{} - {} - {}'.format(self.pk, self.protocolo_entrega.pk, self.produto)
