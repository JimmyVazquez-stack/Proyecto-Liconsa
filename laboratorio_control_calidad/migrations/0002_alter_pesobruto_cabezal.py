# Generated by Django 4.2 on 2024-06-28 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0002_planta_producto_tipoproducto_turno_silo_proveedor_and_more'),
        ('laboratorio_control_calidad', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pesobruto',
            name='cabezal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.cabezal'),
        ),
    ]
