from django.db import models

# Create your models here.


class Tablero(models.Model):
    """
        Se define la clase de Tableros
    """
    campos = models.TextField(default="Pendiente,En curso,Terminado")
    tipo_us = models.OneToOneField('tipo_us.MiembroTipoUs', on_delete=models.CASCADE, null=True, blank=True)
