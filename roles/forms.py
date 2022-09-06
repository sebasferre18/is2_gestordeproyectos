from .models import Rol
from django import forms


class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = [
            'nombre',
            'descripcion',
            'permiso'
        ]
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
            'permiso': 'Permisos',
        }
        widgets = {
            'permiso': forms.CheckboxSelectMultiple(),
        }


