from django.db import models
from django.utils import timezone
from catalogos.models import Cabezal, Planta, Producto, Maquina, Proveedor, Silo, Turno
from usuarios.models import Usuario

# Create your models here.
class EncabTablaR49(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    observaciones = models.CharField(verbose_name="Observaciones",max_length=512, blank=True) 

    def __str__(self):
       return f"ID: {self.id}, fecha: {self.fecha}"
    

#Encabezado para formularios normales    
class EncabR49V2(models.Model):
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
    linea = models.CharField( max_length=40, blank=True) #concatenacion string de los campos planta, turno,silo y cabezal
    densidad = models.DecimalField(default=0, max_digits=5, decimal_places=4)
    volumen = models.IntegerField(default=0, verbose_name=" Volumen")
    encabezado = models.ForeignKey(EncabR49V2, on_delete=models.CASCADE, null=True)

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
    encabezado = models.ForeignKey(EncabR49V2, on_delete=models.CASCADE, null=True)

    def __str__(self):
        pass
    
class Pesobruto(models.Model):
    fechaHora = models.DateTimeField(default=timezone.now,verbose_name="Hora")
    cabezal = models.ForeignKey(Cabezal, on_delete=models.CASCADE, null=True)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, null=True) 
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE, null=True)
    valor = models.IntegerField(default=0)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE) #relacion hacia modelo Usuario de app Usuarios
    encabezado = models.ForeignKey(EncabR49V2, on_delete=models.CASCADE, null=True)

    def __str__(self):
        pass



# Create your models here.

class LecheReconsSilosEncab(models.Model):
    folio = models.IntegerField()
    periodo_Ini = models.DateField(default=timezone.now)
    periodo_Fin = models.DateField(default=timezone.now)
    observaciones = models.CharField(verbose_name="Observaciones",max_length=512, blank=True) 

    class Meta:
        verbose_name_plural = "Encabezado de Leche Reconstituida en Silos"

# Create your models here.
class terminadoEncab(models.Model):
    folio = models.IntegerField()
    fecha = models.DateField(default=timezone.now)
    estatus = models.BooleanField(default = True)

    def __str__(self):
       return f"ID: {self.id}, Folio: {self.folio}"
    
    class Meta:
        verbose_name_plural = "Encabezado de Producto Terminado"

    
class LecheReconsSilos(models.Model):
    OPCIONES = [(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),]
    encabezado = models.ForeignKey(LecheReconsSilosEncab,on_delete=models.CASCADE,null=True)
    fecha_Hora = models.DateTimeField(default=timezone.now,verbose_name="Hora")
    silo = models.ForeignKey(Silo,on_delete=models.CASCADE,verbose_name="No. Silo",null=True)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE,verbose_name="Tipo de Producto", null=True)
    volumen = models.FloatField(default=0.0,verbose_name=" Volumen")
    aspecto = models.IntegerField(choices=OPCIONES,verbose_name="Aspecto")
    sabor = models.IntegerField(choices=OPCIONES,verbose_name="Sabor")
    olor = models.IntegerField(choices=OPCIONES,verbose_name="Olor")
    temperatura = models.FloatField(default=0.0,verbose_name="Temperatura")
    ph = models.FloatField(default=0.0,verbose_name="PH")
    acidez = models.FloatField(default=0.0,verbose_name="Acidez")
    densidad = models.FloatField(default=0.0,verbose_name="Densidad")
    s_g_w_v = models.FloatField(default=0.0,verbose_name="s_g_w_v")
    s_n_g_Stsg_wv = models.FloatField(default=0.0,verbose_name="s_n_g_Stsg_wv")
    st_wv = models.FloatField(default=0.0,verbose_name="st_wv")
    proteina = models.FloatField(default=0.0,verbose_name="Proteína")

    def __str__(self):
       return f"Encabezado_Id: {self.encabezado}, Hora: {self.fecha_Hora}, Producto: {self.producto}, Volumen: {self.volumen}"

    class Meta:
        verbose_name_plural = "Leche Reconstituida en Silos"



    
class producto_terminado(models.Model):
    lotCad = models.CharField(max_length=10, verbose_name="Fecha de caducidad")
    planta = models.ForeignKey(Planta, max_length=10, on_delete=models.CASCADE, verbose_name="Planta")
    turno = models.ForeignKey(Turno, max_length=10, on_delete=models.CASCADE, verbose_name="Turno")
    silo = models.ForeignKey(Silo, on_delete=models.CASCADE, verbose_name="Silo")
    maquina = models.ForeignKey(Maquina, max_length=10, on_delete=models.CASCADE, verbose_name="Máquina")
    hora = models.TimeField(default=timezone.now, verbose_name="Hora")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Tipo de muestra")
    volumen = models.FloatField(default=0.0, verbose_name="Volumen")
    choice = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    aspecto = models.IntegerField(choices=choice, verbose_name="Aspecto")
    sabor = models.IntegerField(choices=choice,null=True, verbose_name="Sabor")
    olor = models.IntegerField(choices=choice,null=True, verbose_name="Olor")
    temperatura = models.FloatField(default=0.0, verbose_name="Temperatura")
    acidez = models.FloatField(default=0.0, verbose_name="Ácidez")
    densidad = models.FloatField(default=0.0, verbose_name="Densidad")
    sg = models.FloatField(default=0.0, verbose_name="S.G")
    sng = models.FloatField(default=0.0, verbose_name="S.N.G")
    st = models.FloatField(default=0.0, verbose_name="S.T")
    proteina = models.FloatField(default=0.0, verbose_name="Proteína")
    encabezado = models.ForeignKey(terminadoEncab, on_delete=models.CASCADE, verbose_name="Folio")

    def __str__(self):
        return f"Encabezado_Id: {self.encabezado}, Hora: {self.hora}, Producto: {self.producto}, Volumen: {self.volumen}"

 

#Calidad microbiologica
class CalidadMicrobiologicaEncabezado(models.Model):
    folio = models.IntegerField()
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de Creación", auto_now_add=True)
    observaciones = models.CharField(verbose_name="Observaciones",max_length=512, blank=True) 

    def __str__(self):
       return f"Folio: {self.folio}"
    class Meta:
        verbose_name_plural = "Encabezado de Calidad Microbiológica"

class CalidadMicrobiologica(models.Model):
    fechaHora = models.DateTimeField(default=timezone.now,verbose_name="Hora")
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, max_length=4)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True) 
    organismos_coliformes = models.FloatField(default=0, max_length=30)
    encabezado = models.ForeignKey(CalidadMicrobiologicaEncabezado, on_delete=models.CASCADE)

    def __str__(self):
        return f"Fecha: {self.fechaHora} - {self.planta} - {self.producto}"
    class Meta:
        verbose_name_plural = "Calidad Microbiológica"
#Calidad microbiologica