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

    def __init__(self, *args, **kwargs):
        """Funcion que excluye aquellos permisos que son administrativos"""
        super(RolForm, self).__init__(*args, **kwargs)
        self.fields['permiso'].queryset = Permiso.objects.all().exclude(es_admin=True)


class PermisoForm(forms.ModelForm):
    """Formulario generico con los campos del modelo Permiso"""
    class Meta:
        model = Permiso
        fields = [
            'nombre',
            'es_admin'
        ]
        labels = {
            'nombre': 'Nombre',
            'es_admin': 'Es permiso administrativo',
        }
