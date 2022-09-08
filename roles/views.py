from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Rol, Permiso
from .forms import RolForm, PermisoForm

"""
Vistas de la app de Roles.
"""


@login_required
def index(request):
    """
    Clase de la vista de la lista de Roles
    """
    roles = Rol.objects.all().order_by('id')
    context = {
        'role_list': roles
    }
    return render(request, 'roles/index.html', context)


@login_required
def crear_rol(request):
    """
    Clase de la vista para la creacion de un nuevo Rol.
    """
    form = RolForm()
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/roles/')

    context = {
        'form': form
    }
    return render(request, 'roles/rol_form.html', context)


@login_required
def modificar_rol(request, rol_id):
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

    context = {
        'form': form
    }
    return render(request, 'roles/rol_form.html', context)


@login_required
def eliminar_rol(request, rol_id):
    """Clase de la vista para eliminar un rol"""
    rol = get_object_or_404(Rol, pk=rol_id)
    if request.method == 'POST':
        rol.delete()
        return redirect('/roles/')

    context = {
        'rol': rol
    }
    return render(request, 'roles/eliminar_rol.html', context)


@login_required
def permiso_index(request):
    """
    Clase de la vista de la lista de Permisos
    """
    permisos = Permiso.objects.all().order_by('id')
    context = {
        'permiso_list': permisos
    }
    return render(request, 'roles/permiso_index.html', context)


@login_required
def crear_permiso(request):
    """
    Clase de la vista para la creacion de un nuevo Permiso.
    """
    form = PermisoForm()
    if request.method == 'POST':
        form = PermisoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/roles/')

    context = {
        'form': form
    }
    return render(request, 'roles/permiso_form.html', context)

