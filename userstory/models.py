from django.db import models

class UserStory(models.Model):
    """
    Se define la clase de User Stories
    """
    nombre = models.CharField(max_length=50)
    tipo_us = models.ForeignKey('tipo_us.MiembroTipoUs', on_delete=models.PROTECT)
    descripcion = models.TextField(null=True)
    horas_estimadas = models.PositiveIntegerField(null=True)
    horas_estimadas_original = models.PositiveIntegerField(null=True)
    user_point = models.PositiveIntegerField(null=True)
    business_value = models.PositiveIntegerField(null=True)
    sprint_previo = models.IntegerField(null=True, default=0)
    prioridad = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    autor = models.TextField(null=True)
    aprobado = models.BooleanField(default=False)
    fecha_creacion = models.DateField(blank=True, null=True)
    fecha_modificacion = models.DateField(blank=True, null=True)
    proyecto = models.ForeignKey('proyectos.Proyecto', on_delete=models.CASCADE, null=True, blank=True)
    #Datos del sprint
    sprint = models.ForeignKey('sprints.Sprint', on_delete=models.PROTECT, null=True, blank=True)
    #xD
    estado = models.TextField(default="Pendiente")
    asignado = models.BooleanField(default=False)

    def __str__(self):
        """
        Metodo que retorna el nombre del User Story actual
        :return: retorna el valor del campo nombre del objeto actual
        """
        return self.nombre


class Nota(models.Model):
    userstory = models.ForeignKey(UserStory, on_delete=models.CASCADE, null=False, blank=False)
    creador = models.ForeignKey('proyectos.Miembro', on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateTimeField(blank=True, null=True)
    mensaje = models.TextField(null=True)


class Tarea(models.Model):
    userstory = models.ForeignKey(UserStory, on_delete=models.CASCADE, null=False, blank=False)
    creador = models.ForeignKey('proyectos.Miembro', on_delete=models.CASCADE, null=True, blank=True)
    horas_trabajadas = models.PositiveIntegerField(null=True)
    mensaje = models.TextField(null=True)
    fecha = models.DateTimeField(blank=True, null=True)


class TareaAux(models.Model):
    sprint = models.ForeignKey('sprints.Sprint', on_delete=models.PROTECT, null=True, blank=True)
    fecha = models.DateTimeField(blank=True, null=True)
    horas_trabajadas = models.PositiveIntegerField(default=0)
    horas_estimadas_diferencia = models.PositiveIntegerField(default=0)
