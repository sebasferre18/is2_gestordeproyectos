from django.db import models


# Create your models here.
class Permiso(models.Model):
    '''Define la clase de permisos'''
    nombre = models.CharField(max_length=70, blank=False, null=False)

    def __str__(self):
        return self.nombre


class Rol(models.Model):
    permiso = models.ManyToManyField('Permiso', blank=False)
    nombre = models.CharField(max_length=50, unique=True, blank=False, null=False)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

