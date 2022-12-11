# Generated by Django 4.0.6 on 2022-10-27 00:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Cadastro', '0021_delete_criarsolicitacao'),
        ('estoque', '0017_alter_estoqueitens_destino'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estoqueitens',
            name='destino',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='destino', to='Cadastro.local'),
            preserve_default=False,
        ),
    ]