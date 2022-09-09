from django import forms
from proyectos.models import Proyecto

class ProyectoForm(forms.ModelForm):
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