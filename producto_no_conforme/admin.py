from django.contrib import admin
from .models import Rotos, Lecheria, Poblacion, Ruta


class RotosAdmin(admin.ModelAdmin):
    verbose_name = "Roto"
    verbose_name_plural = "Roto"

class RutaAdmin(admin.ModelAdmin):
    verbose_name = "Ruta"
    verbose_name_plural = "Rutas"

class LecheriaAdmin(admin.ModelAdmin):
    verbose_name = "Lecheria"
    verbose_name_plural = "Lecherias"

class PoblacionAdmin(admin.ModelAdmin):
    verbose_name = "Poblacion"
    verbose_name_plural = "Poblaciones"

admin.site.register(Rotos, RotosAdmin)
admin.site.register(Ruta, RutaAdmin)
admin.site.register(Lecheria, LecheriaAdmin)
admin.site.register(Poblacion, PoblacionAdmin)