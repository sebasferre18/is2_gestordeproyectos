from django import forms
from proyectos.models import Proyecto, Miembro
from roles.models import Rol
from django.forms import inlineformset_factory

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
            'rol'
        ]
        widgets = {
            'rol': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        self.pro_id = kwargs.pop('pro_id', None)
        super(MiembroForm, self).__init__(*args, **kwargs)
        self.fields['rol'].queryset = Rol.objects.filter(proyecto_id=self.pro_id)


class MiembroUsuarioForm(forms.ModelForm):
    """Formulario generico con los campos del modelo Miembro"""
    class Meta:
        model = Miembro
        fields = [
            'usuario'
        ]
        labels = {
            'usuario': 'Scrum Master',
        }


MiembroFormSet = inlineformset_factory(Proyecto, Miembro, form=MiembroUsuarioForm, can_delete=False, extra=1)
