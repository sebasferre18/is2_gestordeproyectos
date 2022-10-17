from django import forms
from .models import Sprint

class SprintForm(forms.ModelForm):
    """Formulario generico con los campos del modelo Sprint"""
    class Meta:
        model = Sprint

        fields = [
            'nombre',
            'descripcion',
            'duracion',
            'capacidad',
        ]

        labels = {
            'nombre':'Nombre',
            'descripcion':'Descripción de Sprint',
            'duracion':'Duración estimada (en dias)',
            'capacidad':'Capacidad calculada',
        }

        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
        }
