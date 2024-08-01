from django.db import models
from django.utils import timezone
from catalogos.models import Cabezal, Planta, Turno, Producto, Proveedor, Silo, Maquina, Area, Analista
from usuarios.models import Usuario

# Create your models here.
class EncabTablaR49(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    observaciones = models.CharField(verbose_name="Observaciones",max_length=512, blank=True) 

    def __str__(self):
       return f"ID: {self.id}, fecha: {self.fecha}"


    
class Densidadpt(models.Model):
    fechaHora = models.DateTimeField (default=timezone.now,verbose_name="Hora")
    cabezal = models.ForeignKey(Cabezal, on_delete=models.CASCADE)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE, null=True)
    silo = models.ForeignKey(Silo, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    linea = models.CharField( max_length=4, blank=True) #concatenacion string de los campos planta, turno,silo y cabezal
    densidad = models.DecimalField(default=0, max_digits=5, decimal_places=4)
    volumen = models.IntegerField(default=0, verbose_name=" Volumen")
    encabezado = models.ForeignKey(EncabTablaR49, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Concatenar los campos y asignar el resultado a 'linea'
        self.linea = f"{self.planta} {self.turno} {self.silo} {self.cabezal}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.linea


class Pesoenvvacio(models.Model):
    fechaHora = models.DateTimeField(default=timezone.now,verbose_name="Hora")
    cabezal = models.ForeignKey(Cabezal, on_delete=models.CASCADE)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE) 
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE) 
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    peso = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    encabezado = models.ForeignKey(EncabTablaR49, on_delete=models.CASCADE)

    def __str__(self):
        pass
    
class Pesobruto(models.Model):
    fechaHora = models.DateTimeField(default=timezone.now,verbose_name="Hora")
    cabezal = models.ForeignKey(Cabezal, on_delete=models.CASCADE, null=True)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, null=True) 
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE, null=True)
    analista = models.ForeignKey(Analista, on_delete=models.CASCADE, null=True)
    valor = models.IntegerField(default=0)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE) #relacion hacia modelo Usuario de app Usuarios
    encabezado = models.ForeignKey(EncabTablaR49, on_delete=models.CASCADE, null=True)

    def __str__(self):
        pass

