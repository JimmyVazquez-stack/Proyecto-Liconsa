# Generated by Django 4.2 on 2024-07-29 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lecheria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('nombre', models.CharField(max_length=50)),
                ('responsable', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Lecherias',
            },
        ),
        migrations.CreateModel(
            name='Planta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('ubicacion', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=100)),
                ('contacto', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Plantas',
            },
        ),
        migrations.CreateModel(
            name='Poblacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('municipio', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Poblaciones',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('numero', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Rutas',
            },
        ),
        migrations.CreateModel(
            name='TipoProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Tipos de productos',
            },
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('matutino', 'Matutino'), ('vespertino', 'Vespertino')], max_length=100)),
                ('descripcion', models.CharField(max_length=100)),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Turnos',
            },
        ),
        migrations.CreateModel(
            name='Silo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(unique=True)),
                ('capacidad', models.DecimalField(decimal_places=2, max_digits=10)),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.planta')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.producto')),
            ],
            options={
                'verbose_name_plural': 'Silos',
            },
        ),
        migrations.CreateModel(
            name='Rotos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_venta', models.DateField()),
                ('fecha_evaluacion', models.DateField()),
                ('rotos_reportados', models.IntegerField()),
                ('lecheria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.lecheria')),
            ],
            options={
                'verbose_name_plural': 'Rotos',
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('contacto', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=100)),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.planta')),
            ],
            options={
                'verbose_name_plural': 'Proveedores',
            },
        ),
        migrations.AddField(
            model_name='producto',
            name='tipo_producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.tipoproducto'),
        ),
        migrations.CreateModel(
            name='Maquina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.planta')),
            ],
            options={
                'verbose_name_plural': 'Maquinas',
            },
        ),
        migrations.AddField(
            model_name='lecheria',
            name='poblacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.poblacion'),
        ),
        migrations.AddField(
            model_name='lecheria',
            name='ruta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.ruta'),
        ),
        migrations.CreateModel(
            name='Cabezal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('maquina', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='catalogos.maquina')),
            ],
            options={
                'verbose_name_plural': 'Cabezales',
            },
        ),
    ]
