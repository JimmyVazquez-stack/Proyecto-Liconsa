from django import forms 
from .models import *
from django.forms import inlineformset_factory


class EncabTablaR49Form(forms.ModelForm):
    class Meta:
        model = EncabTablaR49
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class' : 'form-control'})


#Enabezado ara formularios simples(noformset)
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
        fields = ['fechaHora','cabezal', 'planta', 'producto', 'silo', 'turno', 'linea', 'densidad','volumen']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

class PesoenvvacioForm(forms.ModelForm):
    class Meta:
        model = Pesoenvvacio
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

class PesobrutoForm(forms.ModelForm):
    class Meta:
        model = Pesobruto
        fields = ['fechaHora', 'cabezal', 'maquina', 'planta', 'producto', 'valor', 'usuario']
        
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

#FORMSET PAR LA TABLA R49 START
# DensidadptFormSet = inlineformset_factory(EncabTablaR49, Densidadpt, fields='__all__', extra=7, can_delete=False)
# PesoenvvacioFormSet = inlineformset_factory(EncabTablaR49, Pesoenvvacio, fields='__all__', extra=10, can_delete=False)
# PesobrutoFormSet = inlineformset_factory(EncabTablaR49, Pesobruto, fields='__all__', extra=10, can_delete=False)

from django import forms 
from .models import producto_terminado
from django import forms 
from django.forms import inlineformset_factory
from .models import *

class TerminadoEncabForm(forms.ModelForm):
    
    class Meta:
        model = terminadoEncab
        exclude = ('estatus',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

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
