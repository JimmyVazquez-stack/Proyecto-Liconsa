from django import forms
from .models import Ruta, Poblacion, Lecheria, Rotos


class LecheriaForm(forms.ModelForm):
    class Meta:
        model = Lecheria
        fields = '__all__'