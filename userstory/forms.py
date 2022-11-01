from django import forms

from tipo_us.models import MiembroTipoUs
from .models import UserStory

class US_Form(forms.ModelForm):
    """Formulario generico con los campos del modelo UserStory"""
    class Meta:
        model = UserStory

        fields = [
            'nombre',
            'tipo_us',
            'descripcion',
            'horas_estimadas',
            'user_point',
            'business_value',
        ]

        labels = {
            'nombre':'Nombre',
            'tipo_us':'Tipo de US',
            'descripcion':'Descripcion',
            'horas_estimadas':'Horas estimadas',
            'user_point':'Prioridad tecnica',
            'business_value':'Prioridad de negocio',
        }

        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            #'tipo_us' : forms.TextInput(attrs={'class':'form-control'}),
            'horas_estimadas' : forms.TextInput(attrs={'class':'form-control'}),
            'user_point' : forms.TextInput(attrs={'class':'form-control'}),
            'business_value' : forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        """Funcion que filtra la seleccion de roles.
        Esto hace que solamente puedan elegirse los roles del proyecto actual."""
        self.pro_id = kwargs.pop('pro_id', None)
        super(US_Form, self).__init__(*args, **kwargs)
        self.fields['tipo_us'].queryset = MiembroTipoUs.objects.filter(proyecto_id=self.pro_id)

