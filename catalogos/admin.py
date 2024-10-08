from django.contrib import admin
from .models import Lecheria, Ruta, Poblacion, Rotos, Producto, Planta, Proveedor, Maquina, Cabezal, Turno, Silo, TipoProducto
from django.forms import TimeInput
from .forms import TurnoForm
from django.db import models

# Register your models here.
admin.site.register(Lecheria)
admin.site.register(Ruta)
admin.site.register(Poblacion)
admin.site.register(Rotos)
admin.site.register(Producto)
admin.site.register(Planta)
admin.site.register(Proveedor)
admin.site.register(Maquina)
admin.site.register(Cabezal)
admin.site.register(Silo)
admin.site.register(TipoProducto)

class TurnoAdmin(admin.ModelAdmin):
    form= TurnoForm
    formfield_overrides = {
        models.TimeField: {'widget': TimeInput(attrs={'type': 'time'})},
    }
    
admin.site.register(Turno, TurnoAdmin)

'''
Turno admin con TimeInput para que se muestre el campo de tiempo en el admin
'''
