from django.db import models

# Create your models here.

class Proyecto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    scrum_master = models.CharField(max_length=50)
