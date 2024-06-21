from django.db import models
from django.utils import timezone

# Create your models here.

class LecheReconsSilosEncab(models.Model):
    folio = models.IntegerField()
    periodo_Ini = models.DateField(default=timezone.now)
    periodo_Fin = models.DateField(default=timezone.now)
    observaciones = models.CharField(verbose_name="Observaciones",max_length=512, blank=True) 

    def __str__(self):
       return f"ID: {self.id}, Folio: {self.folio}"
    
class LecheReconsSilos(models.Model):
    OPCIONES = [(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),]
    NO_SILO = [(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),]
    TIPO_PRODUCTO = [('LPD', 'LPD'),('MLGVRG', 'MLGVRG'),('FRISIA', 'FRISIA'),]
    encabezado = models.ForeignKey(LecheReconsSilosEncab,on_delete=models.CASCADE,)
    fecha_Hora = models.DateTimeField(default=timezone.now,verbose_name="Hora")
    silo_Numero = models.IntegerField(choices=NO_SILO,verbose_name="No. Silo" )
    producto = models.CharField(choices=TIPO_PRODUCTO,verbose_name="Tipo de Producto",max_length=10)
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