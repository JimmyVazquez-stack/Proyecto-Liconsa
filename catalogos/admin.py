from django.contrib import admin
from .models import Lecheria, Ruta, Poblacion, Rotos
from laboratorio_control_calidad.models import Densidadpt, Pesoenvvacio, Pesobruto, EncabTablaR49 #Pesoneto
from .models import Lecheria, Ruta, Poblacion, Rotos, Area, Producto, Planta, Proveedor, Maquina, Cabezal, Turno, Silo, TipoProducto, Analista

# Register your models here.
admin.site.register(Lecheria)
admin.site.register(Ruta)
admin.site.register(Poblacion)
admin.site.register(Rotos)



# admin.site.register(Pesoneto)
admin.site.register(Area)
admin.site.register(Producto)
admin.site.register(Planta)
admin.site.register(Proveedor)
admin.site.register(Maquina)
admin.site.register(Cabezal)
admin.site.register(Turno)
admin.site.register(Silo)
admin.site.register(TipoProducto)
admin.site.register(Analista)