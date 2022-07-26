# Generated by Django 4.0.6 on 2022-07-24 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cadastro', '0003_alter_produtos_cod_produto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produtos',
            name='cod_produto',
            field=models.CharField(default='-', max_length=120, unique=True, verbose_name='CÓD'),
        ),
        migrations.AlterField(
            model_name='produtos',
            name='descricao',
            field=models.TextField(blank=True, max_length=150, null=True, verbose_name='Descrição'),
        ),
    ]
