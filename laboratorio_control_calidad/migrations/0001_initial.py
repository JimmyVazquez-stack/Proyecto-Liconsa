# Generated by Django 4.2 on 2024-07-30 18:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogos', '0002_alter_ruta_numero'),
    ]

    operations = [
        migrations.CreateModel(
            name='EncabTablaR49',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('observaciones', models.CharField(blank=True, max_length=512, verbose_name='Observaciones')),
            ],
        ),
        migrations.CreateModel(
            name='LecheReconsSilosEncab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folio', models.IntegerField()),
                ('periodo_Ini', models.DateField(default=django.utils.timezone.now)),
                ('periodo_Fin', models.DateField(default=django.utils.timezone.now)),
                ('observaciones', models.CharField(blank=True, max_length=512, verbose_name='Observaciones')),
            ],
        ),
        migrations.CreateModel(
            name='TablaR49',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numMaquina', models.CharField(max_length=2)),
                ('numDatos', models.IntegerField()),
                ('promedio', models.IntegerField()),
                ('desvStd', models.IntegerField()),
                ('maximo', models.IntegerField()),
                ('minimo', models.IntegerField()),
            ],
        ),
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
                ('aspecto', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
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
                ('maquina', models.ForeignKey(max_length=10, on_delete=django.db.models.deletion.CASCADE, to='catalogos.maquina')),
                ('planta', models.ForeignKey(max_length=10, on_delete=django.db.models.deletion.CASCADE, to='catalogos.planta')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.producto')),
                ('silo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.silo')),
                ('turno', models.ForeignKey(max_length=10, on_delete=django.db.models.deletion.CASCADE, to='catalogos.turno')),
            ],
        ),
        migrations.CreateModel(
            name='Pesoenvvacio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaHora', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Hora')),
                ('cabezal', models.CharField(default=0, max_length=2, verbose_name='Cabezal')),
                ('maquina', models.IntegerField()),
                ('planta', models.CharField(default=0, max_length=4)),
                ('proveedor', models.CharField(default=0, max_length=30)),
                ('peso', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('encabezado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laboratorio_control_calidad.encabtablar49')),
            ],
        ),
        migrations.CreateModel(
            name='Pesobruto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaHora', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Hora')),
                ('maquina', models.IntegerField(default=0)),
                ('planta', models.CharField(default=0, max_length=4)),
                ('analista', models.CharField(default=0, max_length=30)),
                ('valor', models.IntegerField(default=0)),
                ('cabezal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.cabezal')),
                ('encabezado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laboratorio_control_calidad.encabtablar49')),
            ],
        ),
        migrations.CreateModel(
            name='LecheReconsSilos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_Hora', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Hora')),
                ('volumen', models.FloatField(default=0.0, verbose_name=' Volumen')),
                ('aspecto', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='Aspecto')),
                ('sabor', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='Sabor')),
                ('olor', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='Olor')),
                ('temperatura', models.FloatField(default=0.0, verbose_name='Temperatura')),
                ('ph', models.FloatField(default=0.0, verbose_name='PH')),
                ('acidez', models.FloatField(default=0.0, verbose_name='Acidez')),
                ('densidad', models.FloatField(default=0.0, verbose_name='Densidad')),
                ('s_g_w_v', models.FloatField(default=0.0, verbose_name='s_g_w_v')),
                ('s_n_g_Stsg_wv', models.FloatField(default=0.0, verbose_name='s_n_g_Stsg_wv')),
                ('st_wv', models.FloatField(default=0.0, verbose_name='st_wv')),
                ('proteina', models.FloatField(default=0.0, verbose_name='Proteína')),
                ('encabezado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='laboratorio_control_calidad.lechereconssilosencab')),
                ('producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogos.producto', verbose_name='Tipo de Producto')),
                ('silo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogos.silo', verbose_name='No. Silo')),
            ],
        ),
        migrations.CreateModel(
            name='Densidadpt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaHora', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Hora')),
                ('cabezal', models.CharField(default=0, max_length=2, verbose_name='Cabezal')),
                ('planta', models.CharField(default=0, max_length=4)),
                ('silo', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8')], default=0, verbose_name='No. Silo')),
                ('turno', models.CharField(choices=[('X', 'X matutino'), ('Y', 'Y vespertino')], default=0, max_length=20, verbose_name='Turno')),
                ('linea', models.CharField(blank=True, max_length=20)),
                ('densidad', models.DecimalField(decimal_places=4, default=0, max_digits=5)),
                ('volumen', models.IntegerField(default=0, verbose_name=' Volumen')),
                ('encabezado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laboratorio_control_calidad.encabtablar49')),
            ],
        ),
    ]
