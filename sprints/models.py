from django.db import models

ESTADOS_SPRINT = (
    ('Planificacion', 'Planificacion'),
    ('En ejecucion', 'En ejecucion'),
    ('Finalizado', 'Finalizado'),
    ('Cancelado', 'Cancelado'),
)


class Sprint(models.Model):
    """
    Se define la clase de Sprints
    """
    nombre = models.CharField(max_length=50, unique=False, blank=False, null=False)
    descripcion = models.TextField(blank=True, null=True)
    duracion = models.PositiveIntegerField(null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    proyecto = models.ForeignKey('proyectos.Proyecto', on_delete=models.CASCADE, null=True, blank=True)
    capacidad = models.PositiveIntegerField(null=True)
    estado = models.CharField(max_length=25, choices=ESTADOS_SPRINT, default='Planificacion')

    def __str__(self):
        """
        Metodo que retorna el nombre del Sprint actual
        :return: retorna el valor del campo nombre del objeto actual
        """
        return self.nombre


class Desarrollador(models.Model):
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=False, blank=False)
    miembro = models.ForeignKey('proyectos.Miembro', on_delete=models.CASCADE, null=True, blank=True)
    capacidad_por_dia = models.IntegerField(default=0)
    capacidad_total = models.IntegerField(default=0)
    userstory = models.ManyToManyField('userstory.UserStory', blank=True)

    def __str__(self):
        """
        Metodo que retorna el nombre del Desarrollador actual
        """
        return self.miembro.usuario.user.username
