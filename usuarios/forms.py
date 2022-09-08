from django import forms
from usuarios.models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario

        fields = [
            'nombre',
            'apellido',
            'nombreUsuario',
            'contrasenha',
            'email',
            'fecha_nac',
            'capacidadTrabajo',
        ]

        labels = {
            'nombre':'Nombre',
            'apellido':'Apellido',
            'nombreUsuario':'Usuario',
            'contrasenha':'Contrasenha',
            'email':'email',
            'fecha_nac':'fecha de nacimiento',
            'capacidadTrabajo':'capacidad de trabajo',
        }

        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'apellido' : forms.TextInput(attrs={'class':'form-control'}),
            'nombreUsuario' : forms.TextInput(attrs={'class':'form-control'}),
            'contrasenha' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.TextInput(attrs={'class':'form-control'}),
            'fecha_nac' : forms.TextInput(attrs={'class':'form-control'}),
            'capacidadTrabajo' : forms.TextInput(attrs={'class':'form-control'}),
        }