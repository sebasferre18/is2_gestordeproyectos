from django import forms

from userstory.models import UserStory
from .models import Sprint, Desarrollador


class SprintForm(forms.ModelForm):
    """Formulario generico con los campos del modelo Sprint"""
    class Meta:
        model = Sprint

        fields = [
            'nombre',
            'descripcion',
            'duracion',
        ]

        labels = {
            'nombre':'Nombre',
            'descripcion':'Descripción de Sprint',
            'duracion':'Duración estimada (en dias)',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
        }


class DesarrolladorForm(forms.ModelForm):
    """Formulario generico con los campos del modelo Desarrollador"""
    class Meta:
        model = Desarrollador
        fields = [
            'capacidad_por_dia'
        ]


class AsignarUsForm(forms.ModelForm):
    """Formulario generico para la asignacion de US para un desarrollador"""
    class Meta:
        model = Desarrollador
        fields = [
            'userstory'
        ]
        labels = {
            'userstory':'User Story'
        }
        widgets = {
            'userstory': forms.CheckboxSelectMultiple(),
        }


    def __init__(self, *args, **kwargs):
        """Funcion que filtra la seleccion de US.
        Esto hace que solamente puedan elegirse los US del sprint backlog actual."""
        self.sprint_id = kwargs.pop('sprint_id', None)
        super(AsignarUsForm, self).__init__(*args, **kwargs)
        self.fields['userstory'].queryset = UserStory.objects.filter(sprint_id=self.sprint_id).order_by('prioridad')

