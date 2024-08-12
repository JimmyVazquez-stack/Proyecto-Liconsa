from django.db import models
from django.utils import timezone
from catalogos.models import *

# Create your models here.

class LecheReconsSilosEncab(models.Model):
    folio = models.IntegerField()
    periodo_Ini = models.DateField(default=timezone.now)
    periodo_Fin = models.DateField(default=timezone.now)
    observaciones = models.CharField(verbose_name="Observaciones",max_length=512, blank=True) 

    def __str__(self):
       return f"Folio: {self.folio}"
    
class LecheReconsSilos(models.Model):
    OPCIONES = [(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),]
    encabezado = models.ForeignKey(LecheReconsSilosEncab,on_delete=models.CASCADE,null=True, verbose_name="Folio")
    fecha_Hora = models.DateTimeField(default=timezone.now,verbose_name=" Fecha y Hora")
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

 
