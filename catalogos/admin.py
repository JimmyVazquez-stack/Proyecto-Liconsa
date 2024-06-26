from django.contrib import admin
from .models import Lecheria, Ruta, Poblacion, Rotos
from laboratorio_control_calidad.models import TablaR49, Densidadpt, Pesoenvvacio, Pesobruto #Pesoneto

# Register your models here.
admin.site.register(Lecheria)
admin.site.register(Ruta)
admin.site.register(Poblacion)
admin.site.register(Rotos)

#Modelos FormatoR49
admin.site.register(TablaR49)
admin.site.register(Densidadpt)
admin.site.register(Pesoenvvacio)
admin.site.register(Pesobruto)
# admin.site.register(Pesoneto)