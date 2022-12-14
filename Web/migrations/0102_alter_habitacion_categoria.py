# Generated by Django 4.1.1 on 2022-10-17 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0101_alter_habitacion_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habitacion',
            name='categoria',
            field=models.CharField(choices=[('VIP-1', 'DORMITORIO VIP 1'), ('VIP-2', 'DORMITORIO VIP 2'), ('privada-1', 'DORMITORIO ORO 1'), ('privada-2', 'DORMITORIO ORO 2'), ('compartida-1', 'DORMITORIO PLATA 1'), ('compartida-2', 'DORMITORIO PLATA 2'), ('compartida-3', 'DORMITORIO BRONCE 3'), ('compartida-4', 'DORMITORIO BRONCE 4')], max_length=100),
        ),
    ]
