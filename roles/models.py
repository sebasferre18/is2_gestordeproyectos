from django.db import models

"""
Definicion de los modelos Permiso y Rol dentro de la app de Roles
"""

# Create your models here.
class Permiso(models.Model):
    """
    Se define la clase de permisos
    """
    nombre = models.CharField(max_length=70, blank=False, null=False)
    es_admin = models.BooleanField(default=False)

    def __str__(self):
        """
        Metodo que retorna el nombre del permiso actual
        :return: retorna el valor del campo nombre del objeto actual
        """
        return self.nombre


class Rol(models.Model):
    """
    Se define la clase de roles
    """
    permiso = models.ManyToManyField('Permiso', blank=True)
    nombre = models.CharField(max_length=50, unique=False, blank=False, null=False)
    descripcion = models.TextField(blank=True, null=True)
    proyecto = models.ForeignKey('proyectos.Proyecto', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Metodo que retorna el nombre del rol actual
        :return: retorna el valor del campo nombre del objeto actual
        """
        return self.nombre