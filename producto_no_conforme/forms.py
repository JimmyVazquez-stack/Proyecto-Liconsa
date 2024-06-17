from django import forms

class Rotos(forms.Form):
    fecha_venta = forms.DateField(label='Fecha de venta', widget=forms.SelectDateWidget)
    fecha_evaluacion = forms.DateField(label='Fecha de evaluación', widget=forms.SelectDateWidget)
    rotos_reportados = forms.IntegerField(label='Número de envases rotos reportados')
    OPCIONES_SELLADO = [
        ('horizontal', 'Horizontal'),
        ('vertical', 'Vertical'),
    ]
    sellado = forms.ChoiceField(label='Sellado', choices=OPCIONES_SELLADO, widget=forms.RadioSelect)