from django import forms
from proyectos.models import Proyecto, Miembro

"""
Definicion de los formularios para la gestion de proyectos.
"""


class ProyectoForm(forms.ModelForm):
    """Formulario generico con los campos del modelo Proyecto"""
    class Meta:
        model = Proyecto
        fields = [
            'nombre',
            'descripcion',
        ]
        labels = {
            'nombre':'Nombre',
            'descripcion':'Descripcion',
        }
        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'descripcion' : forms.TextInput(attrs={'class':'form-control'}),
        }


class MiembroForm(forms.ModelForm):
    """Formulario generico con los campos del modelo Miembro"""
    class Meta:
        model = Miembro
        fields = [
            'usuario',
            'rol'
        ]
