# Generated by Django 3.2.4 on 2021-07-18 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0097_reserva'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserva',
            name='empresa',
        ),
    ]