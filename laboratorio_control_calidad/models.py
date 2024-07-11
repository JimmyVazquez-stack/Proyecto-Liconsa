from django.db import models
from django.utils import timezone 
from catalogos.models import *

# Create your models here.
class terminadoEncab(models.Model):
    folio = models.IntegerField()
    fecha = models.DateField(default=timezone.now)
    estatus = models.BooleanField(default = True)

    def __str__(self):
       return f"ID: {self.id}, Folio: {self.folio}"
    
class producto_terminado(models.Model):
    lotCad = models.CharField(max_length=10)
    planta = models.ForeignKey(Planta, max_length=10, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, max_length=10, on_delete=models.CASCADE)
    silo = models.ForeignKey(Silo, on_delete=models.CASCADE)
    maquina = models.ForeignKey(Maquina, max_length=10, on_delete=models.CASCADE)
    hora = models.TimeField(default=timezone.now)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    volumen = models.FloatField(default=0.0)
    choice = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    aspecto = models.IntegerField(choices=choice)
    sabor = models.IntegerField(choices=choice,null=True)
    olor = models.IntegerField(choices=choice,null=True)
    temperatura = models.FloatField(default=0.0)
    acidez = models.FloatField(default=0.0)
    densidad = models.FloatField(default=0.0)
    sg = models.FloatField(default=0.0)
    sng = models.FloatField(default=0.0)
    st = models.FloatField(default=0.0)
    proteina = models.FloatField(default=0.0)
    encabezado = models.ForeignKey(terminadoEncab, on_delete=models.CASCADE)

    def __str__(self):
        return f"Encabezado_Id: {self.encabezado}, Hora: {self.hora}, Producto: {self.producto}, Volumen: {self.volumen}"

 