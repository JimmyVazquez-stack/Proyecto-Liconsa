from django.db import models
from django.utils import timezone
from catalogos.models import Cabezal, Planta, Producto, Maquina

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

    class Meta:
        verbose_name_plural = "Encabezado de Leche Reconstituida en Silos"

# Create your models here.
class terminadoEncab(models.Model):
    folio = models.IntegerField()
    fecha = models.DateField(default=timezone.now)
    estatus = models.BooleanField(default = True)

    def __str__(self):
       return f"Folio: {self.folio}"
    
    class Meta:
        verbose_name_plural = "Encabezado de Producto Terminado"

    
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

    class Meta:
        verbose_name_plural = "Leche Reconstituida en Silos"




class terminadoEncab(models.Model): 
    folio = models.IntegerField()
    fecha = models.DateField(default=timezone.now)
    estatus = models.BooleanField(default = True)

    def __str__(self):
       return f" Folio: {self.folio}"
    
class producto_terminado(models.Model):
    lotCad = models.CharField(max_length=10, verbose_name="Fecha de caducidad")
    planta = models.ForeignKey(Planta, max_length=10, on_delete=models.CASCADE, verbose_name="Planta")
    turno = models.ForeignKey(Turno, max_length=10, on_delete=models.CASCADE, verbose_name="Turno")
    silo = models.ForeignKey(Silo, on_delete=models.CASCADE, verbose_name="Silo")
    maquina = models.ForeignKey(Maquina, max_length=10, on_delete=models.CASCADE, verbose_name="Máquina")
    hora = models.TimeField(default=timezone.now, verbose_name="Hora")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Tipo de muestra")
    volumen = models.FloatField(default=0.0, verbose_name="Volumen")
    choice = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    aspecto = models.IntegerField(choices=choice, verbose_name="Aspecto")
    sabor = models.IntegerField(choices=choice,null=True, verbose_name="Sabor")
    olor = models.IntegerField(choices=choice,null=True, verbose_name="Olor")
    temperatura = models.FloatField(default=0.0, verbose_name="Temperatura")
    acidez = models.FloatField(default=0.0, verbose_name="Ácidez")
    densidad = models.FloatField(default=0.0, verbose_name="Densidad")
    sg = models.FloatField(default=0.0, verbose_name="S.G")
    sng = models.FloatField(default=0.0, verbose_name="S.N.G")
    st = models.FloatField(default=0.0, verbose_name="S.T")
    proteina = models.FloatField(default=0.0, verbose_name="Proteína")
    encabezado = models.ForeignKey(terminadoEncab, on_delete=models.CASCADE, verbose_name="Folio")

    def __str__(self):
        return f"Encabezado_Id: {self.encabezado}, Hora: {self.hora}, Producto: {self.producto}, Volumen: {self.volumen}"

 
