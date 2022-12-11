# Generated by Django 4.0.6 on 2022-10-16 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Cadastro', '0017_delete_auxiliar'),
        ('estoque', '0010_remove_estoqueitens_local'),
    ]

    operations = [
        migrations.AddField(
            model_name='estoqueitens',
            name='local',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Local', to='Cadastro.local'),
            preserve_default=False,
        ),
    ]