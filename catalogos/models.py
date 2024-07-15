from django.db import models
from django.core.exceptions import ValidationError 
from datetime import time
'''
Importamos ValidationError para poder validar los datos que se ingresan en los campos de los modelos.
'''
class Ruta(models.Model):
    nombre = models.CharField(max_length=50)
    numero = models.IntegerField()
        
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Rutas"
    
    
class Poblacion(models.Model):
    nombre = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
    class Meta:
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
        verbose_name_plural = "Lecherias"

    
class Rotos(models.Model):
    fecha_venta = models.DateField()
    fecha_evaluacion = models.DateField()
    lecheria = models.ForeignKey(Lecheria, on_delete=models.CASCADE)    
    rotos_reportados = models.IntegerField()

    def __str__(self):
        return '%s : %s' %(self.lecheria, self.rotos_reportados)
    
    class Meta:
        verbose_name_plural = "Rotos"
        


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
        verbose_name_plural = "Proveedores"
        
class Maquina(models.Model):
    numero = models.IntegerField()
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"Maquina {self.numero} "
    
    class Meta:
        verbose_name_plural = "Maquinas"

class Cabezal(models.Model):
    nombre = models.CharField(max_length=100)
    maquina = models.OneToOneField(Maquina, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.maquina}"
    
    class Meta:
        verbose_name_plural = "Cabezales"

    
 
class TipoProducto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Tipos de productos"
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.tipo_producto}"

    class Meta:
        verbose_name_plural = "Productos"

class Turno(models.Model):
    TURNOS_CHOICES = [
        ('matutino', 'Matutino'),
        ('vespertino', 'Vespertino'),
        # Agrega más turnos aquí si es necesario
    ]
    nombre = models.CharField(max_length=100, choices=TURNOS_CHOICES)
    descripcion = models.CharField(max_length=100)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        if self.nombre == 'matutino':
            return "X"
        elif self.nombre == 'vespertino':
            return "Y"
        else:
            # Retorna una nomenclatura genérica si se agregan más turnos en el futuro
            return self.get_nombre_display()

    def clean(self):
        # Define la hora límite para el turno matutino
        hora_limite = time(14, 0)  # 2:00 PM

        # Verifica si el turno es matutino y alguna de las horas excede la hora límite
        if self.nombre == 'matutino' and (self.hora_inicio >= hora_limite or self.hora_fin > hora_limite):
            raise ValidationError('El turno matutino no puede tener horas de inicio o fin después de las 2:00 PM.')

        if self.nombre == 'vespertino' and (self.hora_inicio < hora_limite or self.hora_fin <= hora_limite):
            raise ValidationError('El turno vespertino no puede tener horas de inicio o fin antes de las 2:00 PM.')

    def save(self, *args, **kwargs):
        self.clean()  # Llama a la validación personalizada
        super().save(*args, **kwargs)  # Llama al método save original

    class Meta:
        verbose_name_plural = "Turnos"
        
class Silo(models.Model):
    numero = models.IntegerField(unique=True) #Numero de silo unico
    capacidad = models.DecimalField(max_digits=10, decimal_places=2)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    

    def __str__(self):
        return str(self.numero)
    
    class Meta:
        verbose_name_plural = "Silos"
