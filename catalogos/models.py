from django.db import models
from django.core.exceptions import ValidationError 
'''
Importamos ValidationError para poder validar los datos que se ingresan en los campos de los modelos.
'''
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

#Modelo usado en usuarios
class Area(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Areas"
        


#Modelos generales y reportes
class Planta(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Planta"
        verbose_name_plural = "Plantas"

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Proveedor"
        verbose_name_plural = "Proveedores"
class Maquina(models.Model):
    nombre = models.CharField(max_length=100)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Maquina"
        verbose_name_plural = "Maquinas"

class Cabezal(models.Model):
    codigo = models.CharField(max_length=100)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)

    def __str__(self):
        return self.codigo
    
    class Meta:
        verbose_name_plural = "Cabezal"
        verbose_name_plural = "Cabezales"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Producto"
        verbose_name_plural = "Productos"
class Turno(models.Model):
    descripcion = models.CharField(max_length=100)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return self.descripcion
    
    class Meta:
        verbose_name_plural = "Turno"
        verbose_name_plural = "Turnos"

class Silo(models.Model):
    numero = models.IntegerField()
    capacidad = models.DecimalField(max_digits=10, decimal_places=2)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"Silo {self.numero}"
    
    class Meta:
        verbose_name_plural = "Silo"
        verbose_name_plural = "Silos"