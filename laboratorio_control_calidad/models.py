from django.db import models
from django.utils import timezone 

# Create your models here.
class producto_terminado(models.Model):
    lotCad = models.CharField(max_length=10)
    planta = models.CharField(max_length=10)
    turno = models.CharField(max_length=10)
    silo_choice = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'), 
    ]
    silo = models.IntegerField(choices=silo_choice)
    maquina = models.CharField(max_length=10)
    hora = models.TimeField(default=timezone.now)
    producto_choice = [
           (1, 'LPD'),
           (2, 'MLGVRG'),
           (3, 'FRISIA'),
    ]
    producto = models.IntegerField(choices=producto_choice)
    volumen = models.FloatField()
    aspecto = models.CharField(max_length=30)
    sabor_choice = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    sabor = models.IntegerField(choices=sabor_choice)
    olor_choice = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    olor = models.IntegerField(choices=olor_choice)
    temperatura =models.FloatField()
    acidez =models.FloatField()
    densidad = models.FloatField()
    sg = models.FloatField()
    sng = models.FloatField()
    st = models.FloatField()
    proteina = models.FloatField()
    estatus = models.BooleanField(default = True)

    def __str__(self):
        return "%s %s %s %s" % (self.producto, self.volumen, self.aspecto, self.sabor)


 