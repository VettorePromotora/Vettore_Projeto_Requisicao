# Generated by Django 4.0.6 on 2022-09-06 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0012_alter_perfil_grupo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='grupo',
        ),
    ]