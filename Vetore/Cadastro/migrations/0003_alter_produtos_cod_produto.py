# Generated by Django 4.0.6 on 2022-07-24 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cadastro', '0002_remove_produtos_detalhes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produtos',
            name='cod_produto',
            field=models.IntegerField(default=0, unique=True, verbose_name='CÓD'),
        ),
    ]
