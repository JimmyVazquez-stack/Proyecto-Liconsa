# Generated by Django 4.2 on 2024-10-05 23:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('laboratorio_control_calidad', '0004_alter_densidadpt_linea'),
    ]

    operations = [
        migrations.AlterField(
            model_name='densidadpt',
            name='fechaHora',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha/Hora'),
        ),
        migrations.AlterField(
            model_name='pesobruto',
            name='fechaHora',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha/Hora'),
        ),
        migrations.AlterField(
            model_name='pesoenvvacio',
            name='fechaHora',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha/Hora'),
        ),
    ]