from django import forms
from proyectos.models import Proyecto

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto

        fields = [
            'nombre',
            'descripcion',
            'scrum_master',

        ]

        labels = {
            'nombre':'Nombre',
            'descripcion':'Descripcion',
            'scrum_master':'Scrum Master',
        }

        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'descripcion' : forms.TextInput(attrs={'class':'form-control'}),
            'scrum_master' : forms.TextInput(attrs={'class':'form-control'}),
        }