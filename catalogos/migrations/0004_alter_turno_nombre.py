# Generated by Django 4.2 on 2024-08-12 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0003_alter_silo_numero_alter_silo_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='nombre',
            field=models.CharField(choices=[('Matutino', 'Matutino'), ('Vespertino', 'Vespertino')], max_length=100, unique=True),
        ),
    ]
