# Generated by Django 4.0.6 on 2022-08-21 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0003_remove_perfil_setor'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='permissao',
            field=models.CharField(choices=[('Matriz', 'Matriz'), ('Filial', 'Filial')], max_length=20, null=True, verbose_name='Permissão'),
        ),
    ]