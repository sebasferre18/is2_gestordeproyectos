from django.db import models
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario
from .models import Rol, Permiso
from .forms import RolForm, PermisoForm
from funciones import obtener_permisos

"""
Pruebas de los modelos Permiso y Rol dentro de la app de Roles
"""

# Create your models here.
class TestPermiso(models.Model):
    """
    Se define la clase de permisos
    """
    nombre = models.CharField(max_length=70, blank=False, null=False)

    def __str__(self):
        """
        Metodo que retorna el nombre del permiso actual
        :return: retorna el valor del campo nombre del objeto actual
        """
        return self.nombre


class TestRol(models.Model):
    """
    Se define la clase de roles
    """
    permiso = models.ManyToManyField('Permiso', blank=False)
    nombre = models.CharField(max_length=50, unique=True, blank=False, null=False)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        Metodo que retorna el nombre del rol actual
        :return: retorna el valor del campo nombre del objeto actual
        """
        return self.nombre



def test_index(request):
    """
    Clase de la vista de la lista de Roles
    """
    roles = Rol.objects.all().order_by('id')
    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    context = {
        'role_list': roles,
        'permisos': permisos
    }
    return render(request, 'roles/index.html', context)



def test_crear_rol(request):
    """
    Clase de la vista para la creacion de un nuevo Rol.
    """
    form = RolForm()
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/roles/')

    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    context = {
        'form': form,
        'permisos': permisos
    }
    return render(request, 'roles/crear_rol.html', context)



def test_modificar_rol(request, rol_id):
    """
    Clase de la vista para la modificacion de un Rol
    """
    rol = get_object_or_404(Rol, pk=rol_id)
    form = RolForm(instance=rol)

    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            form.save()
            return redirect('/roles/')

    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    context = {
        'form': form,
        'permisos': permisos
    }
    return render(request, 'roles/modificar_rol.html', context)



def test_eliminar_rol(request, rol_id):
    """Clase de la vista para eliminar un rol"""
    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    rol = get_object_or_404(Rol, pk=rol_id)
    if request.method == 'POST':
        rol.delete()
        return redirect('/roles/')

    context = {
        'rol': rol,
        'permisos': permisos
    }
    return render(request, 'roles/eliminar_rol.html', context)



def test_permiso_index(request):
    """
    Clase de la vista de la lista de Permisos
    """
    permisos = Permiso.objects.all().order_by('id')

    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    p = obtener_permisos(rol)

    context = {
        'permiso_list': permisos,
        'permisos': p
    }
    return render(request, 'roles/permiso_index.html', context)



def test_crear_permiso(request):
    """
    Clase de la vista para la creacion de un nuevo Permiso.
    """
    form = PermisoForm()
    if request.method == 'POST':
        form = PermisoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/permissions/')

    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    p = obtener_permisos(rol)

    context = {
        'form': form,
        'permisos': p
    }
    return render(request, 'roles/permiso_form.html', context)

