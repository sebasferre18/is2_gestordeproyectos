from django import forms

from userstory.models import UserStory, Tarea, Nota

ch = (
    ("1", "One"),
)


class ActualizarEstadoForm(forms.ModelForm):
    """Formulario generico para la actualizacion del estado de un US dentro de un tablero"""

    class Meta:
        model = UserStory
        fields = [
            'estado'
        ]
        labels = {
            'estado':'Estado siguiente'
        }
        widgets = {
            'estado': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        """Funcion que da como opcion los estados siguientes de un US dentro de un tablero."""
        self.estados_siguientes = kwargs.pop('estados_siguientes', None)
        super(ActualizarEstadoForm, self).__init__(*args, **kwargs)
        self.fields['estado'] = forms.ChoiceField(choices=tuple(self.estados_siguientes))


class TareaForm(forms.ModelForm):
    """Formulario generico con los campos del modelo Tarea"""
    class Meta:
        model = Tarea

        fields = [
            'horas_trabajadas',
            'mensaje',
        ]
        labels = {
            'horas_trabajadas':'Horas trabajadas',
            'mensaje':'Mensaje adjunto a registrar',
        }


class NotaForm(forms.ModelForm):
    """Formulario generico con los campos del modelo Nota"""
    class Meta:
        model = Nota

        fields = [
            'mensaje',
        ]
        labels = {
            'mensaje':'Mensaje adjunto a registrar',
        }