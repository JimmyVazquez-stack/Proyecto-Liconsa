from django.db import models
from django.utils import timezone

# Create your models here.
class EncabTablaR49(models.Model):
    fecha = models.DateField(default=timezone.now)
    observaciones = models.CharField(verbose_name="Observaciones",max_length=512, blank=True) 

    def __str__(self):
       return f"ID: {self.id}, fecha: {self.fecha}"



class TablaR49(models.Model):
    numMaquina = models.CharField(max_length=2)
    numDatos = models.IntegerField()
    promedio = models.IntegerField()
    desvStd = models.IntegerField()
    maximo = models.IntegerField()
    minimo = models.IntegerField()

    def __str__(self):
        return '%s - %s' % (self.numMaquina, self.promedio)
    
class Densidadpt(models.Model):
    NO_SILO = [(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),]
    TURNOS = [('X', 'X matutino'),('Y', 'Y vespertino'),]
    fechaHora = models.DateTimeField (default=timezone.now,verbose_name="Hora")
    cabezal = models.CharField(default=0, verbose_name="Cabezal", max_length=2) #cambiar a modelos lalo
    planta = models.CharField(default=0, max_length=4) #cambiar a modelos lalo
    # producto = models.ForeignKey(producto,on_delete=models.CASCADE, null=True) #colocar cuando lalo cree los modelos de producto
    silo = models.IntegerField(default=0,choices=NO_SILO,verbose_name="No. Silo")
    turno = models.CharField(default=0,choices=TURNOS,verbose_name='Turno', max_length=20)
    linea = models.CharField( max_length=20, blank=True) #concatenacion string de los campos planta, turno,silo y cabezal
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
    cabezal = models.CharField(default=0, verbose_name="Cabezal",max_length=2) #cambiar a modelos lalo
    maquina = models.IntegerField() #cambiar a modelos lalo
    planta = models.CharField(default=0, max_length=4) #cambiar a modelos lalo
    # producto = models.ForeignKey(producto,on_delete=models.CASCADE, null=True) #colocar cuando lalo cree los modelos de producto
    proveedor = models.CharField(default=0, max_length=30) #cambiar a modelos lalo
    peso = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    encabezado = models.ForeignKey(EncabTablaR49, on_delete=models.CASCADE)

    def __str__(self):
        pass
    
class Pesobruto(models.Model):
    fechaHora = models.DateTimeField(default=timezone.now,verbose_name="Hora")
    cabezal = models.CharField(default=0, max_length=2) #cambiar a modelos lalo
    maquina = models.IntegerField(default=0) #cambiar a modelos lalo
    planta = models.CharField(default=0, max_length=4) #cambiar a modelos lalo
    # producto = models.ForeignKey(producto,on_delete=models.CASCADE, null=True) #colocar cuando lalo cree los modelos de producto
    analista = models.CharField(default=0, max_length=30) #cambiar a modelos lalo
    valor = models.IntegerField(default=0)
    encabezado = models.ForeignKey(EncabTablaR49, on_delete=models.CASCADE)

    def __str__(self):
        pass

