<<<<<<< HEAD
# Generated by Django 4.2 on 2024-06-09 02:33
=======
# Generated by Django 4.2 on 2024-06-12 18:06
>>>>>>> d2087161ed664a5d99d597d283d3efa8089d7dc6

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
