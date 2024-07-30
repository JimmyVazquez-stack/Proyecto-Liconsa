from django.db import models
from django.contrib.auth.models import (AbstractUser)


class Area(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Areas"

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=10, null=True)
    area=models.ForeignKey(Area, on_delete=models.CASCADE, null=True)
    
    def __str__(self): 
        return self.username
    
    class Meta:
        verbose_name_plural = "Usuarios"
        
    
    


