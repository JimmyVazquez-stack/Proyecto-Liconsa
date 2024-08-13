from django.db import models

# Create your models here.
class ModeloTemporal(models.Model):
    volumen = models.FloatField()
    temperatiura = models.FloatField()
    densidadgml = models.FloatField()  
    grasasgl = models.FloatField()
    snggl = models.FloatField()
    proteinagl = models.FloatField()
    ph = models.FloatField()

    def __str__(self):
        return f'{self.volumen} - {self.temperatiura} - {self.densidadgml} - {self.grasasgl} - {self.snggl} - {self.proteinagl} - {self.ph}'
    
class ModeloTemporal2(models.Model):
    volumen = models.FloatField()
    temperatiura = models.FloatField()
    densidadgml = models.FloatField()  
    grasasgl = models.FloatField()
    snggl = models.FloatField()
    proteinagl = models.FloatField()
    ph = models.FloatField()

    def __str__(self):
        return f'{self.volumen} - {self.temperatiura} - {self.densidadgml} - {self.grasasgl} - {self.snggl} - {self.proteinagl} - {self.ph}'
