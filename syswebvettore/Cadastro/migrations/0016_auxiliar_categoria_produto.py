# Generated by Django 4.0.6 on 2022-10-15 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Cadastro', '0015_alter_auxiliar_local_produto_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auxiliar',
            name='categoria_produto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Cadastro.categoria'),
        ),
    ]