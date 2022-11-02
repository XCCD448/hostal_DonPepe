# Generated by Django 3.2.4 on 2021-07-18 19:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Web', '0096_delete_reserva'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateTimeField()),
                ('check_out', models.DateTimeField()),
                ('estado', models.CharField(choices=[('APROBADA', 'Aprobada'), ('CANCELADA', 'Cancelada')], default='APROBADA', max_length=150)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Web.empresa')),
                ('habitacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Web.habitacion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]