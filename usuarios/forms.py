from django import forms
from usuarios.models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario

        fields = [
            'user',
            'fecha_nac',
            'capacidadTrabajo',
        ]

        labels = {
            'user':'Usuario',
            'fecha_nac':'fecha de nacimiento',
            'capacidadTrabajo':'capacidad de trabajo',
        }

        widgets = {
            'fecha_nac' : forms.TextInput(attrs={'class':'form-control'}),
            'capacidadTrabajo' : forms.TextInput(attrs={'class':'form-control'}),
        }