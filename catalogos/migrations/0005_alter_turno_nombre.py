# Generated by Django 4.2 on 2024-08-12 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0004_alter_turno_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='nombre',
            field=models.CharField(choices=[('Matutino', 'Matutino'), ('Vespertino', 'Vespertino')], max_length=100),
        ),
    ]
