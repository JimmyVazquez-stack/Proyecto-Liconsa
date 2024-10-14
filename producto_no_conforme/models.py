from django.db import models
from django.utils import timezone 
from catalogos.models import *

class MalSelladosEncab(models.Model):
    programaSocial = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Tipo de muestra")
    fechaVenta = models.DateField(default=timezone.now, verbose_name="Fecha de venta")
    fechaEvaluacion = models.DateField(default=timezone.now, verbose_name="Fecha de evaluación")

    def __str__(self):
       return f" Id: {self.id}"
    
class MalSellados(models.Model):
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, verbose_name="Ruta")
    lecheria = models.ForeignKey(Lecheria, on_delete=models.CASCADE, verbose_name="Lecheria")
    colonia = models.CharField(max_length=50, verbose_name="Colonia o Localidad")
    noRotos = models.IntegerField()
    choiceSellado = [(1, 'Horizontal'), (2, 'Vertical')]
    sellado = models.IntegerField(choices=choiceSellado, verbose_name="Sellado")
    choiceImputfabricacion = [(1, 'Perforado sist. de envasado'), (2, 'Picado por canastilla'), (3, 'Polietileno picado'), (4, 'Bolsa chica')]
    imputFabricacion = models.IntegerField(choices=choiceImputfabricacion, verbose_name="Imputables a la fabricación")
    choiceImputransportacion = [(1, 'Pellizco por canastilla'), (2, 'Por Gancho'), (3, 'Caida estiba')]
    imputTransportacion = models.IntegerField(choices=choiceImputransportacion, verbose_name="Imputables a la transportación")
    choiceCausInt = [(1, 'Envase mordido'), (2, 'Cortado')]
    causInt = models.IntegerField(choices=choiceCausInt, verbose_name="Causas intencionales")
    encabezado = models.ForeignKey(MalSelladosEncab, on_delete=models.CASCADE)

    def __str__(self):
        return f"Encabezado_Id: {self.MalSelladosencab}, Id: {self.id}"