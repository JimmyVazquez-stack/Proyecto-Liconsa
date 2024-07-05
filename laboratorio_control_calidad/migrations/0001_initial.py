# Generated by Django 4.2 on 2024-07-04 19:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogos', '0006_analista'),
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
            name='Pesoenvvacio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaHora', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Hora')),
                ('peso', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('cabezal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.cabezal')),
                ('encabezado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laboratorio_control_calidad.encabtablar49')),
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
                ('analista', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogos.analista')),
                ('cabezal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogos.cabezal')),
                ('encabezado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='laboratorio_control_calidad.encabtablar49')),
                ('maquina', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogos.maquina')),
                ('planta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogos.planta')),
                ('producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogos.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Densidadpt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaHora', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Hora')),
                ('linea', models.CharField(blank=True, max_length=4)),
                ('densidad', models.DecimalField(decimal_places=4, default=0, max_digits=5)),
                ('volumen', models.IntegerField(default=0, verbose_name=' Volumen')),
                ('cabezal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.cabezal')),
                ('encabezado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laboratorio_control_calidad.encabtablar49')),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.planta')),
                ('producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogos.producto')),
                ('silo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.silo')),
                ('turno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.turno')),
            ],
        ),
    ]
