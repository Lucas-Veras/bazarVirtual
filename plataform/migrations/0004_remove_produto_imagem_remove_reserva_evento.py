# Generated by Django 4.0.4 on 2022-08-06 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plataform', '0003_alter_produto_imagem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='imagem',
        ),
        migrations.RemoveField(
            model_name='reserva',
            name='evento',
        ),
    ]
