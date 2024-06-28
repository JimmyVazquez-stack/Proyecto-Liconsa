from django.db import models

# Create your models here.
class PuntosDeEvaluacion(models.Model):
    nombre = models.CharField(max_length=100)

class ComposicionFisioquimica(models.Model):
    nombre = models.ForeignKey(PuntosDeEvaluacion, on_delete=models.CASCADE)
    volumen = models.FloatField()
    temperatiura = models.FloatField()
    densidadgml = models.FloatField()  
    grasasgl = models.FloatField()
    snggl = models.FloatField()
    proteinagl = models.FloatField()
    ph = models.FloatField()

    def __str__(self):
        return f'{self.volumen} - {self.temperatiura} - {self.densidadgml} - {self.grasasgl} - {self.snggl} - {self.proteinagl} - {self.ph}'
    
class DatosDeProduccion(models.Model):
   ProduccionReal = models.FloatField()
   ProduccionVentas = models.FloatField()