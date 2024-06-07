from django.db import models
    
class Ruta(models.Model):
    nombre = models.CharField(max_length=50)
    numero = models.IntegerField()

    class Meta:
        verbose_name = "Ruta"
        verbose_name_plural = "Rutas"
    
    def __str__(self):
        return self.nombre
    
    
class Poblacion(models.Model):
    nombre = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Poblacion"
        verbose_name_plural = "Poblaciones"

    def __str__(self):
        return self.nombre
    
class Lecheria(models.Model):
    numero = models.IntegerField()
    nombre = models.CharField(max_length=50)
    responsable = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    poblacion = models.ForeignKey(Poblacion, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Lecheria"
        verbose_name_plural = "Lecherias"

    def __str__(self):
        return '%s - %s - %s - %s' % (self.numero, self.nombre, self.ruta, self.poblacion)
    
class Rotos(models.Model):
    fecha_venta = models.DateField()
    fecha_evaluacion = models.DateField()
    lecheria = models.ForeignKey(Lecheria, on_delete=models.CASCADE)    
    rotos_reportados = models.IntegerField()

    class Meta:
        verbose_name = "Roto"
        verbose_name_plural = "Rotos"   

    def __str__(self):
        return self.rotos_reportados