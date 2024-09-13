from django import forms
from distribucion.models import EncabOrdenDesp, OrdenDespPNC


#[INICIO]Formularios Orden despacho--------------------------------------------------------#
class EncabOrdenDespForm(forms.ModelForm):
    class Meta:
        model = EncabOrdenDesp
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

class OrdenDespForm(forms.ModelForm):
    
    class Meta:
        model = OrdenDespPNC
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class' : 'form-control'})
        
#[FIN]Formularios Orden despacho---------------------------------------------------#