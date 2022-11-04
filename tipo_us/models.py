from django.db import models
from proyectos.models import Proyecto

# Create your models here.

class Tipo_US(models.Model):
    """
    Se define la clase de tipos de User Stories
    """
    nombre = models.CharField(max_length=50)
    fecha_creacion = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=50)
    campos = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        Metodo que retorna el nombre del tipo de US actual
        :return: retorna el valor del campo nombre del objeto actual
        """
        return self.nombre

    def crear_tipo_us(self, nombre, fecha_creacion, descripcion):
        return self.crear_tipo_us(nombre, fecha_creacion, descripcion)

class MiembroTipoUs(models.Model):
    """
    Se define la clase de tipos de User Stories por proyecto
    """
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=False, blank=False)
    tipo_us = models.ForeignKey(Tipo_US, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Metodo que retorna el nombre del tipo de US actual de un proyecto en especifico
        :return: retorna el valor del campo nombre del objeto actual
        """
        return self.tipo_us.nombre

