from django.db import models

class UserStory(models.Model):
    """
    Se define la clase de User Stories
    """
    nombre = models.CharField(max_length=50)
    tipo_us = models.ForeignKey('tipo_us.MiembroTipoUs', on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=50)
    horas_estimadas = models.PositiveIntegerField(null=True)
    user_point = models.PositiveIntegerField(null=True)
    business_value = models.PositiveIntegerField(null=True)
    sprint_previo = models.IntegerField(null=True, default=0)
    prioridad = models.PositiveIntegerField(null=True)
    autor = models.TextField(null=True)
    aprobado = models.BooleanField(default=False)
    fecha_creacion = models.DateField(blank=True, null=True)
    proyecto = models.ForeignKey('proyectos.Proyecto', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Metodo que retorna el nombre del User Story actual
        :return: retorna el valor del campo nombre del objeto actual
        """
        return self.nombre