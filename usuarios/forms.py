from django import forms
from django.contrib.auth.models import User
from usuarios.models import Usuario
from django.forms import inlineformset_factory


class UserForm(forms.ModelForm):
    class  Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email'
        ]


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'ci',
            'telefono',
            'fecha_nac'
        ]
        labels = {
            'ci':'Cedula',
            'telefono':'Telefono',
            'fecha_nac':'Fecha de nacimiento',
        }
        widgets = {
            'fecha_nac': forms.TextInput(attrs={'class':'form-control'}),
        }


UsuarioFormSet = inlineformset_factory(User, Usuario, form=UsuarioForm, can_delete=False)
