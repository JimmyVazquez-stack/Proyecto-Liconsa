from django.contrib import admin
from .models import Densidadpt, Pesoenvvacio, Pesobruto, EncabTablaR49

# Register your models here.
#Modelos FormatoR49
admin.site.register(Densidadpt)
admin.site.register(Pesoenvvacio)
admin.site.register(Pesobruto)
admin.site.register(EncabTablaR49)
