from django import forms 
from django.forms import inlineformset_factory
from .models import *

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

LecheReconsSilosFormSet = inlineformset_factory(LecheReconsSilosEncab, LecheReconsSilos, fields='__all__', extra=8, can_delete=False)