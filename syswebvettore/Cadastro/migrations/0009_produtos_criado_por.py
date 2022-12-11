# Generated by Django 4.0.6 on 2022-09-05 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Cadastro', '0008_alter_categoria_options_alter_solicitacao_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='produtos',
            name='criado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]