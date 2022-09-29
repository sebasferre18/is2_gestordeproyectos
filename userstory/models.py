from django.db import models

class UserStory(models.Model):
    nombre = models.CharField(max_length=50)
    tipo_us = models.ForeignKey('tipo_us.Tipo_US', on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=50)
    horas_estimadas = models.PositiveIntegerField(null=True)
    user_point = models.PositiveIntegerField(null=True)
    business_value = models.PositiveIntegerField(null=True)
    autor = models.TextField('usuarios.Usuario', null=True)
    aprobado = models.BooleanField(default=False)
    fecha_creacion = models.DateField(blank=True, null=True)
    proyecto = models.ForeignKey('proyectos.Proyecto', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre