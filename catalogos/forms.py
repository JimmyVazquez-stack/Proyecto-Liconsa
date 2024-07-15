from django import forms
from .models import Ruta, Poblacion, Lecheria, Rotos, Turno
from django.core.exceptions import ValidationError
from datetime import time

class LecheriaForm(forms.ModelForm):
    class Meta:
        model = Lecheria
        fields = '__all__'
        



class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['nombre', 'descripcion' ,'hora_inicio', 'hora_fin']

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if Turno.objects.filter(nombre=nombre).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este nombre de turno ya existe.')
        return nombre