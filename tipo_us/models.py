from django.db import models

# Create your models here.

class Tipo_US(models.Model):
    nombre = models.CharField(max_length=50)
    fecha_creacion = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre