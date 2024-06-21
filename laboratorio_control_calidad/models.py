from django.db import models
from django.utils import timezone 

# Create your models here.
class terminadoEncab(models.Model):
    folio = models.IntegerField()
    fecha = models.DateField(default=timezone.now)
    estatus = models.BooleanField(default = True)

    def __str__(self):
       return f"ID: {self.id}, Folio: {self.folio}"
    
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


 