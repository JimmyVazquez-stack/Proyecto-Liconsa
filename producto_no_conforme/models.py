from django.db import models
    
class Ruta(models.Model):
    nombre = models.CharField(max_length=50)
    numero = models.IntegerField()
    
    def __str__(self):
        return self.nombre
    
    
class Poblacion(models.Model):
    numero = models.IntegerField()
    municipio = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return self.municipio
    
    
class Lecheria(models.Model):
    numero = models.IntegerField()
    nombre = models.CharField(max_length=50)
    responsable = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    poblacion = models.ForeignKey(Poblacion, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numero)
    
class Rotos(models.Model):
    fecha_venta = models.DateField()
    fecha_evaluacion = models.DateField()
    lecheria = models.ForeignKey(Lecheria, on_delete=models.CASCADE)    
    rotos_reportados = models.IntegerField()

    def __str__(self):
        return self.rotos_reportados