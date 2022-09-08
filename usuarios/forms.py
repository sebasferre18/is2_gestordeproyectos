from django import forms
from usuarios.models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario

        fields = [
            'user',
            'fecha_nac',
        ]

        labels = {
            'user':'Usuario',
            'fecha_nac':'fecha de nacimiento',
        }

        widgets = {
            'fecha_nac' : forms.TextInput(attrs={'class':'form-control'}),
        }