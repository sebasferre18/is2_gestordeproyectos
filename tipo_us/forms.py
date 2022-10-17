from django import forms
from tipo_us.models import Tipo_US, MiembroTipoUs


class Tipo_usForm(forms.ModelForm):
    """Formulario generico con los campos del modelo Tipo_US"""
    class Meta:
        model = Tipo_US
        fields = [
            'nombre',
            'descripcion',
            'campos',
        ]
        labels = {
            'nombre':'Nombre',
            'descripcion':'Descripcion',
            'campos':'Campos',
        }
        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'descripcion' : forms.TextInput(attrs={'class':'form-control'}),
        }


class MiembroTipoUsForm(forms.ModelForm):
    """Formulario generico con los campos del modelo MiembroTipoUs"""
    class Meta:
        model = MiembroTipoUs
        fields = [
            'tipo_us',
        ]