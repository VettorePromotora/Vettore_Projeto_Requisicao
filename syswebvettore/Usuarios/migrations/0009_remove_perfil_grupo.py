# Generated by Django 4.0.6 on 2022-08-24 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0008_perfil_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='grupo',
        ),
    ]