# Generated by Django 4.2 on 2024-06-12 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('producto_no_conforme', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rotos',
            name='lecheria',
        ),
        migrations.DeleteModel(
            name='Lecheria',
        ),
        migrations.DeleteModel(
            name='Poblacion',
        ),
        migrations.DeleteModel(
            name='Rotos',
        ),
        migrations.DeleteModel(
            name='Ruta',
        ),
    ]
