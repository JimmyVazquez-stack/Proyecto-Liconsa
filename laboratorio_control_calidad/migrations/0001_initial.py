# Generated by Django 4.2 on 2024-06-24 23:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogos', '0002_planta_producto_tipoproducto_turno_silo_proveedor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='terminadoEncab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folio', models.IntegerField()),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('estatus', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='producto_terminado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lotCad', models.CharField(max_length=10)),
                ('hora', models.TimeField(default=django.utils.timezone.now)),
                ('volumen', models.FloatField(default=0.0)),
                ('aspecto', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True)),
                ('sabor', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True)),
                ('olor', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True)),
                ('temperatura', models.FloatField(default=0.0)),
                ('acidez', models.FloatField(default=0.0)),
                ('densidad', models.FloatField(default=0.0)),
                ('sg', models.FloatField(default=0.0)),
                ('sng', models.FloatField(default=0.0)),
                ('st', models.FloatField(default=0.0)),
                ('proteina', models.FloatField(default=0.0)),
                ('encabezado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laboratorio_control_calidad.terminadoencab')),
                ('maquina', models.ForeignKey(max_length=10, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogos.maquina')),
                ('planta', models.ForeignKey(max_length=10, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogos.planta')),
                ('producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogos.producto')),
                ('silo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogos.silo')),
                ('turno', models.ForeignKey(max_length=10, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogos.turno')),
            ],
        ),
    ]