from django.db import models
from roles.models import Rol

"""
Definicion de los modelos Proyecto y Miembro dentro de la app de Proyectos
"""

# Create your models here.

ESTADOS_PROYECTO = (
    ('Planificacion', 'Planificacion'),
    ('En ejecucion', 'En ejecucion'),
    ('Finalizado', 'Finalizado'),
    ('Cancelado', 'Cancelado'),
)

class Proyecto(models.Model):
    """
    Se define la clase de proyectos
    """
    nombre = models.CharField(max_length=50)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=50)
    estado = models.CharField(max_length=25, choices=ESTADOS_PROYECTO, default='Planificacion')

    def __str__(self):
        """
        Metodo que retorna el nombre del proyecto actual
        :return: retorna el valor del campo nombre del objeto actual
        """
        return self.nombre


class Miembro(models.Model):
    """
    Se define la clase de miembros
    """
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=False, blank=False)
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.PROTECT, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True, blank=True)