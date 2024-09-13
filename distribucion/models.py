from django.db import models
from django.utils import timezone
from catalogos.models import Cabezal, Planta, Producto, Maquina, Silo, Turno, Proveedor, Ruta
from usuarios.models import Usuario
from django.core.validators import MinValueValidator

#----------Encabezado para formato orden despacho (PNC)-------------#    
class EncabOrdenDesp(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    observaciones = models.CharField(verbose_name="Observaciones",max_length=512, blank=True) 

    def __str__(self):
       return f"ID: {self.id}, fecha: {self.fecha}"

#-----[START] Modelo para Orden Despacho PNC (TX-HP-854-02-R01)-----------------------------------#
class OrdenDespPNC(models.Model):
    responsRuta =  models.CharField(verbose_name="Responsables rutas",max_length=100, blank=True)
    ruta = models.ForeignKey(Ruta, max_length=10, on_delete=models.CASCADE)
    # programa = models.ForeignKey(, max_length=10, on_delete=models.CASCADE) #crear el modelo programas en catalogos y agregar como foreignkey
    numEcoUnidad = models.IntegerField(default=0)
    tempInicial = models.FloatField(default=0.0)
    dotacion =  models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])#Esto asegura que el valor siempre sea 0 o mayor
    canastillas = models.IntegerField(default=0)
    encabezado = models.ForeignKey(EncabOrdenDesp, on_delete=models.CASCADE, null=True)

    def __str__(self):
       return f"Responsable Ruta: {self.responsRuta}, Tipo: {self.ruta}"

    class Meta:
        verbose_name_plural = "Ordenes de Despacho"
