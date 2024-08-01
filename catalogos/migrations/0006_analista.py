# Generated by Django 4.2 on 2024-07-02 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0005_tipoproducto_rename_codigo_cabezal_nombre_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=100)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.area')),
            ],
            options={
                'verbose_name_plural': 'Analistas',
            },
        ),
    ]