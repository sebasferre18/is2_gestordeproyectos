from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from roles.models import *

"""
Definicion del modelo extendido Usuario dentro la app de Usuarios
"""


# Create your models here.
class Usuario(models.Model):
    """
    Se define la clase de usuarios
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rol = models.ManyToManyField(Rol, blank=True)
    ci = models.IntegerField(blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    fecha_nac = models.DateField(blank=True, null=True)

    def __str__(self):
        """
        Metodo que retorna el nombre del usuario actual
        :return: retorna el valor del campo nombre del objeto actual
        """
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Metodo que crea una instancia del modelo Usuario luego de haber completado el formulario de Crear Usuario
    """
    if created:
        Usuario.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Metodo que guarda la instancia recien creada del modelo Usuario de Django
    """
    instance.usuario.save()