from django.db import models
from django.utils import timezone
from catalogos.models import Cabezal, Planta, Producto, Proveedor, Maquina

# Create your models here.
class EncabTablaR49(models.Model):
    fecha = models.DateField(default=timezone.now)
    observaciones = models.CharField(verbose_name="Observaciones",max_length=512, blank=True) 

    def __str__(self):
       return f"ID: {self.id}, fecha: {self.fecha}"



class TablaR49(models.Model):
    numMaquina = models.CharField(max_length=2)
    numDatos = models.IntegerField()
    promedio = models.IntegerField()
    desvStd = models.IntegerField()
    maximo = models.IntegerField()
    minimo = models.IntegerField()

    def __str__(self):
        return '%s - %s' % (self.numMaquina, self.promedio)
    
class Densidadpt(models.Model):
    NO_SILO = [(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),]
    TURNOS = [('X', 'X matutino'),('Y', 'Y vespertino'),]
    fechaHora = models.DateTimeField (default=timezone.now,verbose_name="Hora")
    cabezal = models.CharField(default=0, verbose_name="Cabezal", max_length=2) #cambiar a modelos lalo
    planta = models.CharField(default=0, max_length=4) #cambiar a modelos lalo
    # producto = models.ForeignKey(producto,on_delete=models.CASCADE, null=True) #colocar cuando lalo cree los modelos de producto
    silo = models.IntegerField(default=0,choices=NO_SILO,verbose_name="No. Silo")
    turno = models.CharField(default=0,choices=TURNOS,verbose_name='Turno', max_length=20)
    linea = models.CharField( max_length=20, blank=True) #concatenacion string de los campos planta, turno,silo y cabezal
    densidad = models.DecimalField(default=0, max_digits=5, decimal_places=4)
    volumen = models.IntegerField(default=0, verbose_name=" Volumen")
    encabezado = models.ForeignKey(EncabTablaR49, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Concatenar los campos y asignar el resultado a 'linea'
        self.linea = f"{self.planta} {self.turno} {self.silo} {self.cabezal}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.linea


class Pesoenvvacio(models.Model):
    fechaHora = models.DateTimeField(default=timezone.now,verbose_name="Hora")
    cabezal = models.CharField(default=0, verbose_name="Cabezal",max_length=2) #cambiar a modelos lalo
    maquina = models.IntegerField() #cambiar a modelos lalo
    planta = models.CharField(default=0, max_length=4) #cambiar a modelos lalo
    # producto = models.ForeignKey(producto,on_delete=models.CASCADE, null=True) #colocar cuando lalo cree los modelos de producto
    proveedor = models.CharField(default=0, max_length=30) #cambiar a modelos lalo
    peso = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    encabezado = models.ForeignKey(EncabTablaR49, on_delete=models.CASCADE)

    def __str__(self):
        pass
    
class Pesobruto(models.Model):
    fechaHora = models.DateTimeField(default=timezone.now,verbose_name="Hora")
    cabezal = models.ForeignKey(Cabezal, on_delete=models.CASCADE) #cambiar a modelos lalo
    maquina = models.IntegerField(default=0) #cambiar a modelos lalo
    planta = models.CharField(default=0, max_length=4) #cambiar a modelos lalo
    # producto = models.ForeignKey(producto,on_delete=models.CASCADE, null=True) #colocar cuando lalo cree los modelos de producto
    analista = models.CharField(default=0, max_length=30) #cambiar a modelos lalo
    valor = models.IntegerField(default=0)
    encabezado = models.ForeignKey(EncabTablaR49, on_delete=models.CASCADE)

    def __str__(self):
        pass

from catalogos.models import *

# Create your models here.

class LecheReconsSilosEncab(models.Model):
    folio = models.IntegerField()
    periodo_Ini = models.DateField(default=timezone.now)
    periodo_Fin = models.DateField(default=timezone.now)
    observaciones = models.CharField(verbose_name="Observaciones",max_length=512, blank=True) 
from django.utils import timezone 

# Create your models here.
class terminadoEncab(models.Model):
    folio = models.IntegerField()
    fecha = models.DateField(default=timezone.now)
    estatus = models.BooleanField(default = True)

    def __str__(self):
       return f"ID: {self.id}, Folio: {self.folio}"
    
class LecheReconsSilos(models.Model):
    OPCIONES = [(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),]
    encabezado = models.ForeignKey(LecheReconsSilosEncab,on_delete=models.CASCADE,null=True)
    fecha_Hora = models.DateTimeField(default=timezone.now,verbose_name="Hora")
    silo = models.ForeignKey(Silo,on_delete=models.CASCADE,verbose_name="No. Silo",null=True)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE,verbose_name="Tipo de Producto", null=True)
    volumen = models.FloatField(default=0.0,verbose_name=" Volumen")
    aspecto = models.IntegerField(choices=OPCIONES,verbose_name="Aspecto")
    sabor = models.IntegerField(choices=OPCIONES,verbose_name="Sabor")
    olor = models.IntegerField(choices=OPCIONES,verbose_name="Olor")
    temperatura = models.FloatField(default=0.0,verbose_name="Temperatura")
    ph = models.FloatField(default=0.0,verbose_name="PH")
    acidez = models.FloatField(default=0.0,verbose_name="Acidez")
    densidad = models.FloatField(default=0.0,verbose_name="Densidad")
    s_g_w_v = models.FloatField(default=0.0,verbose_name="s_g_w_v")
    s_n_g_Stsg_wv = models.FloatField(default=0.0,verbose_name="s_n_g_Stsg_wv")
    st_wv = models.FloatField(default=0.0,verbose_name="st_wv")
    proteina = models.FloatField(default=0.0,verbose_name="Proteína")

    def __str__(self):
       return f"Encabezado_Id: {self.encabezado}, Hora: {self.fecha_Hora}, Producto: {self.producto}, Volumen: {self.volumen}"
class producto_terminado(models.Model):
    lotCad = models.CharField(blank=True, max_length=10)
    planta = models.CharField(blank=True, max_length=10)
    turno = models.CharField(blank=True, max_length=10)
    silo_choice = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), ]
    silo = models.IntegerField(choices=silo_choice, blank=True, null=True)
    maquina = models.CharField(blank=True, max_length=10)
    hora = models.TimeField(default=timezone.now)
    producto_choice = [(1, 'LPD'),(2, 'MLGVRG'),(3, 'FRISIA'),]
    producto = models.IntegerField(choices=producto_choice, blank=True, null=True)
    volumen = models.FloatField(default=0.0)
    aspecto = models.CharField(blank=True, max_length=30)
    sabor_choice = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),]
    sabor = models.IntegerField(choices=sabor_choice, blank=True, null=True)
    olor_choice = [(1, '1'), (2, '2'),(3, '3'),(4, '4'),(5, '5'),]
    olor = models.IntegerField(choices=olor_choice, blank=True, null=True)
    temperatura =models.FloatField(default=0.0)
    acidez =models.FloatField(default=0.0)
    densidad = models.FloatField(default=0.0)
    sg = models.FloatField(default=0.0)
    sng = models.FloatField(default=0.0)
    st = models.FloatField(default=0.0)
    proteina = models.FloatField(default=0.0)
    encabezado = models.ForeignKey(terminadoEncab,on_delete=models.CASCADE,)

    def __str__(self):
        return "%s %s %s %s" % (self.producto, self.volumen, self.aspecto, self.sabor)


 
