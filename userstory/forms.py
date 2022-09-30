from django import forms
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
            'autor',
            'aprobado',
            'fecha_creacion',
        ]

        labels = {
            'nombre':'nombre',
            'tipo_us':'Tipo de user story',
            'descripcion':'descripcion',
            'horas_estimadas':'horas estimadas',
            'user_point':'user point',
            'business_value':'business value',
            'autor':'autor',
            'aprobado':'aprobado',
            'fecha_creacion':'fecha de creacion',
        }

        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            #'tipo_us' : forms.TextInput(attrs={'class':'form-control'}),
            'descripcion' : forms.TextInput(attrs={'class':'form-control'}),
            'horas_estimadas' : forms.TextInput(attrs={'class':'form-control'}),
            'user_point' : forms.TextInput(attrs={'class':'form-control'}),
            'business_value' : forms.TextInput(attrs={'class':'form-control'}),
            'autor' : forms.TextInput(attrs={'class':'form-control'}),
            'aprobado' : forms.TextInput(attrs={'class':'form-control'}),
            'fecha_creacion' : forms.TextInput(attrs={'class':'form-control'}),
        }