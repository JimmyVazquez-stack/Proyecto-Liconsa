from django.db import models

# Create your models here.


class TablaR49(models.Model): 
    num_maquina = models.CharField(max_length=2) 
    num_datos = models.IntegerField() 
    promedio = models.IntegerField() 
    desv_std = models.IntegerField() 
    maximo = models.IntegerField() 
    minimo = models.IntegerField() 

 
    def __str__(self): 
     return '%s - %s' % (self.num_maquina, self.promedio) 