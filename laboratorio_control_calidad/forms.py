from django import forms 
from .models import *
from django.forms import inlineformset_factory


class EncabR49V2Form(forms.ModelForm):
    class Meta:
        model = EncabR49V2
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class' : 'form-control'})



class DensidadptForm(forms.ModelForm):
    class Meta:
        model = Densidadpt
        fields = ['fechaHora','cabezal', 'planta', 'producto', 'silo', 'turno', 'linea', 'densidad','volumen','encabezado']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

class PesoenvvacioForm(forms.ModelForm):
    class Meta:
        model = Pesoenvvacio
        fields = ['fechaHora','cabezal','maquina','planta','producto','proveedor','peso','encabezado']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

class PesobrutoForm(forms.ModelForm):
    class Meta:
        model = Pesobruto
        fields = ['fechaHora', 'cabezal', 'maquina', 'planta', 'producto', 'valor', 'usuario','encabezado']
        
    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor <= 0:
            raise forms.ValidationError("El valor debe ser mayor que cero.")
        return valor
        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

class LecheReconsSilosEncabForm(forms.ModelForm):
    class Meta:
        model = LecheReconsSilosEncab
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

class LecheReconsSilosForm(forms.ModelForm):
    class Meta:
        model = LecheReconsSilos
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

LecheReconsSilosFormSet = inlineformset_factory(LecheReconsSilosEncab, LecheReconsSilos, fields='__all__', extra=6, can_delete=False)




class TerminadoEncabForm(forms.ModelForm):
    
    class Meta:
        model = terminadoEncab
        exclude = ('estatus',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'id': field, 'name': field})



class TerminadoForm(forms.ModelForm):
    
    class Meta:
        model = producto_terminado
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class' : 'form-control'})


class permisosForm(forms.ModelForm):
    
    status = [
    ('True','Permitido edición'),
    ('False','No se puede editar')
    ]
    estatus = forms.ChoiceField(choices=status,widget=forms.RadioSelect)



    class Meta:
        model = producto_terminado
        fields = [
            'id',
            'estatus',
            ]
        
        labels = {
            'id':'id',
            'estatus':'Permisos',
        }

        
TerminadoFormSet = inlineformset_factory(terminadoEncab, producto_terminado, fields='__all__', extra=3, can_delete=False) 
LecheReconsSilosFormSet = inlineformset_factory(LecheReconsSilosEncab, LecheReconsSilos, fields='__all__', extra=8, can_delete=False)
TerminadoFormSet = inlineformset_factory(terminadoEncab, producto_terminado, fields='__all__', extra=3, can_delete=False)    







#Formulario Calidad Microbiologica
class CalidadMicrobiologicaEncabezadoForm(forms.ModelForm):
    class Meta:
        model = CalidadMicrobiologicaEncabezado
        fields = ['folio']

class CalidadMicrobiologicaForm(forms.ModelForm):
    class Meta:
        model = CalidadMicrobiologica
        fields = ['fechaHora', 'planta', 'producto', 'organismos_coliformes', 'encabezado']
