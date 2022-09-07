from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    nombreUsuario = models.CharField(max_length=50)
    contrasenha = models.CharField(max_length=50)
    email = models.EmailField()
    fecha_nac = models.DateField()
    capacidadTrabajo = models.IntegerField()

