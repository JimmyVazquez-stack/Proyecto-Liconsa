from django.db import models
from django.core.exceptions import ValidationError 
from datetime import datetime, time

'''
Importamos ValidationError para poder validar los datos que se ingresan en los campos de los modelos.
'''
class Ruta(models.Model):
    nombre = models.CharField(max_length=50)
    numero = models.IntegerField(unique=True)
        
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

#Modelo usado en usuarios
# class Area(models.Model):
#     nombre = models.CharField(max_length=50)
#     descripcion = models.CharField(max_length=50)
    
#     def __str__(self):
#         return self.nombre
    
#     class Meta:
#         verbose_name_plural = "Areas"
        


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
        return f"{self.numero} - {self.planta}"

    class Meta:
        verbose_name_plural = "Máquinas"
        unique_together = ('numero', 'planta')  # Asegura que el número sea único por planta

class Cabezal(models.Model):
    nombre = models.CharField(
        max_length=1,
        help_text="Ingrese una letra de la A a la F. A y B para la máquina 1, C y D para la máquina 2, E y F para la máquina 3."
    )
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Cabezales"
        unique_together = ('nombre', 'maquina')  # Asegurar unicidad por máquina

    def clean(self):
        super().clean()

        # Convertir a mayúsculas para la validación de unicidad
        self.nombre = self.nombre.upper()

        # Definir las letras permitidas para cada máquina
        letras_permitidas = {
            1: ['A', 'B'],
            2: ['C', 'D'],
            3: ['E', 'F'],
            # Permitir letras adicionales si es necesario
        }

        # Validar letras adicionales
        letras_adicionales = 'GHIJKLMNOPQRSTUVWXYZ'

        # Validar el nombre del cabezal y la máquina
        if self.maquina.numero in letras_permitidas:
            if self.nombre not in letras_permitidas[self.maquina.numero] + list(letras_adicionales):
                raise ValidationError(f'El cabezal {self.nombre} no es válido para la máquina {self.maquina.numero}.')
        elif self.nombre not in letras_adicionales:
            raise ValidationError('El nombre del cabezal no está permitido.')

        # Comprobar unicidad del nombre del cabezal para la misma máquina
        if Cabezal.objects.filter(maquina=self.maquina, nombre__iexact=self.nombre).exclude(pk=self.pk).exists():
            raise ValidationError(f'El cabezal {self.nombre} ya existe para la máquina {self.maquina.numero}.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

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
        ('Matutino', 'Matutino'),
        ('Vespertino', 'Vespertino'),
    ]
    nombre = models.CharField(max_length=100, unique=True, choices=TURNOS_CHOICES)
    descripcion = models.TextField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estatus = models.BooleanField(default=True)

    def __str__(self):
        if self.nombre == 'Matutino':
            return "X"
        elif self.nombre == 'Vespertino':
            return "Y"
        else:
            return self.get_nombre_display()

    def clean(self):
        # Define la hora límite para el turno matutino
        hora_limite = time(14, 0)  # 2:00 PM

        # Validación para turnos matutinos
        if self.nombre == 'Matutino':
            if isinstance(self.hora_inicio, str):
                self.hora_inicio = datetime.strptime(self.hora_inicio, '%H:%M').time()
            if isinstance(self.hora_fin, str):
                self.hora_fin = datetime.strptime(self.hora_fin, '%H:%M').time()

            if self.hora_inicio >= hora_limite or self.hora_fin > hora_limite:
                raise ValidationError('El turno matutino no puede tener horas de inicio o fin después de las 2:00 PM.')

        # Validación para turnos vespertinos
        if self.nombre == 'Vespertino':
            if isinstance(self.hora_inicio, str):
                self.hora_inicio = datetime.strptime(self.hora_inicio, '%H:%M').time()
            if isinstance(self.hora_fin, str):
                self.hora_fin = datetime.strptime(self.hora_fin, '%H:%M').time()

            if self.hora_inicio < hora_limite or self.hora_fin <= hora_limite:
                raise ValidationError('El turno vespertino debe comenzar después de las 2:00 PM y terminar antes de las 11:59 PM.')

    def save(self, *args, **kwargs):
        self.clean()  # Llama a la validación personalizada
        super().save(*args, **kwargs)  # Llama al método save original

    class Meta:
        verbose_name_plural = "Turnos"    
        
class Silo(models.Model):
    numero = models.IntegerField()
    capacidad = models.DecimalField(max_digits=10, decimal_places=2)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numero)
    
    class Meta:
        verbose_name_plural = "Silos"
        unique_together = ('numero', 'planta')  # Asegura que el número de silo sea único solo dentro de una planta
