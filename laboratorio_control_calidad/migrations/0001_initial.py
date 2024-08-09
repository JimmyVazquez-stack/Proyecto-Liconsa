# Generated by Django 4.2 on 2024-08-09 20:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Densidadpt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaHora', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Hora')),
                ('linea', models.CharField(blank=True, max_length=4)),
                ('densidad', models.DecimalField(decimal_places=4, default=0, max_digits=5)),
                ('volumen', models.IntegerField(default=0, verbose_name=' Volumen')),
            ],
        ),
        migrations.CreateModel(
            name='EncabR49V2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('observaciones', models.CharField(blank=True, max_length=512, verbose_name='Observaciones')),
            ],
        ),
        migrations.CreateModel(
            name='EncabTablaR49',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('observaciones', models.CharField(blank=True, max_length=512, verbose_name='Observaciones')),
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
            ],
            options={
                'verbose_name_plural': 'Leche Reconstituida en Silos',
            },
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
            options={
                'verbose_name_plural': 'Encabezado de Leche Reconstituida en Silos',
            },
        ),
        migrations.CreateModel(
            name='terminadoEncab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folio', models.IntegerField()),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('estatus', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Encabezado de Producto Terminado',
            },
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
                ('peso', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('cabezal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.cabezal')),
                ('encabezado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='laboratorio_control_calidad.encabtablar49')),
                ('maquina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.maquina')),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.planta')),
                ('producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogos.producto')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='Pesobruto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaHora', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Hora')),
                ('valor', models.IntegerField(default=0)),
                ('cabezal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogos.cabezal')),
                ('encabezado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='laboratorio_control_calidad.encabtablar49')),
                ('maquina', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogos.maquina')),
                ('planta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogos.planta')),
                ('producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogos.producto')),
            ],
        ),
    ]
