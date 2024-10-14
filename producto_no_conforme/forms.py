from django import forms
from .models import *

class Rotos(forms.Form):
    fecha_venta = forms.DateField(label='Fecha de venta', widget=forms.SelectDateWidget)
    fecha_evaluacion = forms.DateField(label='Fecha de evaluación', widget=forms.SelectDateWidget)
    rotos_reportados = forms.IntegerField(label='Número de envases rotos reportados')
    OPCIONES_SELLADO = [
        ('horizontal', 'Horizontal'),
        ('vertical', 'Vertical'),
    ]
    sellado = forms.ChoiceField(label='Sellado', choices=OPCIONES_SELLADO, widget=forms.RadioSelect)

class MalSelladosEncabForm(forms.ModelForm):
    
    class Meta:
        model = MalSelladosEncab
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'id': field})

class MalSelladosForm(forms.ModelForm):
    class Meta:
        model = MalSellados
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Filtrar el campo 'lecheria' basado en el campo 'ruta'
        if 'ruta' in self.data:
            try:
                ruta_id = int(self.data.get('ruta'))
                self.fields['lecheria'].queryset = Lecheria.objects.filter(ruta_id=ruta_id)
            except (ValueError, TypeError):
                pass  # Invalid input or no input for ruta
        elif self.instance.pk:
            # Si el formulario está en modo edición
            self.fields['lecheria'].queryset = Lecheria.objects.filter(ruta=self.instance.ruta)






