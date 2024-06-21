from django.db import models
    
class Ruta(models.Model):
    nombre = models.CharField(max_length=50)
    numero = models.IntegerField()
        
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Ruta"
        verbose_name_plural = "Rutas"
    
    
class Poblacion(models.Model):
    nombre = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Poblacion"
        verbose_name_plural = "Poblaciones"
    
class Lecheria(models.Model):
    numero = models.IntegerField()
    nombre = models.CharField(max_length=50)
    responsable = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    poblacion = models.ForeignKey(Poblacion, on_delete=models.CASCADE)
    
    def __str__(self):
        return '%s - %s - %s - %s' % (self.numero, self.nombre, self.ruta, self.poblacion)
    
    class Meta:
        verbose_name_plural = "Lecheria"
        verbose_name_plural = "Lecherias"

    
class Rotos(models.Model):
    fecha_venta = models.DateField()
    fecha_evaluacion = models.DateField()
    lecheria = models.ForeignKey(Lecheria, on_delete=models.CASCADE)    
    rotos_reportados = models.IntegerField()

    def __str__(self):
        return '%s : %s' %(self.lecheria, self.rotos_reportados)
    
    class Meta:
        verbose_name_plural = "Roto"
        verbose_name_plural = "Rotos"
        verbose_name_plural = "Rotos"
        
class Area(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Areas"
