from .models import Rol, Permiso
from django import forms

"""
Definicion de los formularios para la gestion de roles.
"""


class RolForm(forms.ModelForm):
    """Formulario generico con los campos del modelo Rol"""
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


class PermisoForm(forms.ModelForm):
    """Formulario generico con los campos del modelo Permiso"""
    class Meta:
        model = Permiso
        fields = [
            'nombre'
        ]
        labels = {
            'nombre': 'Nombre',
        }

