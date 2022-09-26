from django.db import models
from proyectos.models import Proyecto

# Create your models here.

class Tipo_US(models.Model):
    nombre = models.CharField(max_length=50)
    fecha_creacion = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    def crear_tipo_us(self, nombre, descripcion):
        return self.crear_tipo_us(nombre, descripcion)

class MiembroTipoUs(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=False, blank=False)
    tipo_us = models.ForeignKey(Tipo_US, on_delete=models.CASCADE, null=True, blank=True)
