from django.db import models
from django.contrib.auth.models import (AbstractUser)
from catalogos.models import Area


class Usuario(AbstractUser):
    telefono = models.CharField(max_length=10, null=True)
    area=models.ForeignKey(Area, on_delete=models.CASCADE, null=True)
    
    def __str__(self): 
        return self.username
    
    class Meta:
        verbose_name_plural = "Usuarios"


