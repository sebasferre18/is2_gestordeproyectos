from django import forms
from tipo_us.models import Tipo_US, MiembroTipoUs


class Tipo_usForm(forms.ModelForm):
    class Meta:
        model = Tipo_US
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


class MiembroTipoUsForm(forms.ModelForm):
    class Meta:
        model = MiembroTipoUs
        fields = [
            'tipo_us',
        ]