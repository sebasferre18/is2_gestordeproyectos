from django.db import models


# Create your models here.
class Permission(models.Model):
    '''Define la clase de permisos'''
    name = models.CharField(max_length=70, blank=False, null=False)

    def __str__(self):
        return self.name


class Role(models.Model):
    permission = models.ManyToManyField('Permission', blank=False)
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    def get_id(self):
        return self.id

    def set_name(self, nom):
        self.name = nom

    def set_description(self, desc):
        self.description = desc

    def get_description(self):
        return self.description

    def set_permission(self, per):
        self.permission = per

    def get_permission(self):
        return self.permission

    def list_permission(self):
        permission = self.permission.filter()
        return list(permission)

    def add_permission(self, per):
        self.permission.append(per)

