# Generated by Django 4.1.1 on 2022-10-18 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0103_alter_habitacion_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacto',
            name='asunto',
            field=models.IntegerField(choices=[[0, 'Problema'], [1, 'Reservar'], [2, 'Solicitud'], [3, 'Registro Usuario'], [4, 'Solicitud cambio de contraeña'], [5, 'Cancelar']]),
        ),
    ]