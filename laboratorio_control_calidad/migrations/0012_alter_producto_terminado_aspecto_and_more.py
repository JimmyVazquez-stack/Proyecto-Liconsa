# Generated by Django 4.2 on 2024-07-04 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratorio_control_calidad', '0011_alter_producto_terminado_aspecto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto_terminado',
            name='aspecto',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True),
        ),
        migrations.AlterField(
            model_name='producto_terminado',
            name='olor',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True),
        ),
        migrations.AlterField(
            model_name='producto_terminado',
            name='sabor',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True),
        ),
    ]
