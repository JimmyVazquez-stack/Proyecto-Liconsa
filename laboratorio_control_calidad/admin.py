from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import *

# Register your models here.
admin.site.register(LecheReconsSilosEncab)
admin.site.register(LecheReconsSilos)
admin.site.register(CalidadMicrobiologicaEncabezado)
admin.site.register(CalidadMicrobiologica)

#Modelos FormatoR49
admin.site.register(Densidadpt)
admin.site.register(Pesoenvvacio)
admin.site.register(Pesobruto)
admin.site.register(EncabTablaR49)
admin.site.register(Permission)
