from django import forms
from .models import Sprint, Desarrollador


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


class DesarrolladorForm(forms.ModelForm):
    """Formulario generico con los campos del modelo Desarrollador"""
    class Meta:
        model = Desarrollador
        fields = [
            'capacidad_por_dia'
        ]
        widgets = {
            'capacidad_por_dia': forms.CharField(),
        }