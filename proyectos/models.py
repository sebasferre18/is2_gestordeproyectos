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

ACCION_HISTORIAL = (
    ('Creacion', 'Creacion'),
    ('Modificacion', 'Modificacion'),
    ('Eliminacion', 'Eliminacion'),
    ('Importacion', 'Importacion'),
)

ELEMENTOS = (
    ('Proyectos', 'Proyectos'),
    ('Roles', 'Roles'),
    ('Sprints', 'Sprints'),
    ('Tableros', 'Tableros'),
    ('Tipo de US', 'Tipo de US'),
    ('User Stories', 'User Stories'),
)

class Proyecto(models.Model):
    """
    Se define la clase de proyectos
    """
    nombre = models.CharField(max_length=50)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    descripcion = models.TextField()
    estado = models.CharField(max_length=25, choices=ESTADOS_PROYECTO, default='Planificacion')
    story_points = models.IntegerField(default=0)

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
    rol = models.ManyToManyField(Rol, blank=True)
    userstory = models.ManyToManyField('userstory.UserStory', blank=True)

    def __str__(self):
        """
        Metodo que retorna el nombre del miembro actual
        """
        return self.usuario.user.username


class Historial(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True, blank=True)
    responsable = models.ForeignKey('usuarios.Usuario', on_delete=models.PROTECT, null=True, blank=True)
    fecha = models.DateTimeField(blank=True, null=True)
    accion = models.CharField(max_length=25, choices=ACCION_HISTORIAL, null=True)
    elemento = models.CharField(max_length=25, choices=ELEMENTOS, null=True)
    informacion = models.TextField(null=True)
    userstory = models.ForeignKey('userstory.UserStory', on_delete=models.CASCADE, null=True, blank=True)


class Notificacion(models.Model):
    #proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True, blank=True)
    #responsable = models.ForeignKey('usuarios.Usuario', on_delete=models.PROTECT, null=True, blank=True)
    fecha = models.DateTimeField(blank=True, null=True)
    #accion = models.CharField(max_length=25, choices=ACCION_HISTORIAL, null=True)
    #elemento = models.CharField(max_length=25, choices=ELEMENTOS, null=True)
    informacion = models.TextField(null=True)
    destinatario = models.ForeignKey('usuarios.Usuario', on_delete=models.PROTECT, null=True, blank=True)
    visto = models.BooleanField(default=False)


