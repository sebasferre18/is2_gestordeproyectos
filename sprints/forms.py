from django import forms
from .models import Sprint

class US_Form(forms.ModelForm):
    class Meta:
        model = Sprint

        fields = [
            'nombre',
            'descripcion',
            'duracion',
            'proyecto',
            'capacidad',
        ]

        labels = {
            'nombre':'nombre',
            'descripcion':'Descripción de Sprint',
            'duracion':'Duración estimada',
            'proyecto':'Proyecto',
            'capacidad':'Capacidad calculada',
        }

        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'descripcion' : forms.TextInput(attrs={'class':'form-control'}),
            'duracion' : forms.TextInput(attrs={'class':'form-control'}),
        }