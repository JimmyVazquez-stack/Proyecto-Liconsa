# Generated by Django 4.2 on 2024-06-11 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='telefono',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
