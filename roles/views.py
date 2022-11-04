from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario
from .models import Rol, Permiso
from .forms import RolForm, PermisoForm
from proyectos.models import Proyecto, Miembro
from funciones import obtener_permisos
from django.contrib import messages
"""
Vistas de la app de Roles.
"""


@login_required
def index(request, proyecto_id):
    """
    Clase de la vista de la lista de Roles
    """
    roles = Rol.objects.filter(proyecto_id=proyecto_id).order_by('id')
    proyecto = Proyecto.objects.get(id=proyecto_id)

    user = request.user
    miembros = Miembro.objects.filter(proyecto=proyecto)
    usuario = Usuario.objects.get(user_id=user.id)

    miembro_aux = miembros.get(usuario=usuario, proyecto=proyecto)
    rol = miembro_aux.rol.get_queryset()
    if rol:
        permisos = obtener_permisos(rol)
    else:
        permisos = []

    context = {
        'role_list': roles,
        'permisos': permisos,
        'proyecto_id': proyecto_id,
        'proyecto': proyecto
    }
    return render(request, 'roles/index.html', context)


@login_required
def crear_rol(request, proyecto_id):
    """
    Clase de la vista para la creacion de un nuevo Rol.
    """
    proyecto = Proyecto.objects.get(id=proyecto_id)
    form = RolForm()
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            aux = form.save(commit=False)
            aux.proyecto = proyecto
            aux.save()
            form.save_m2m()
            return redirect('roles:index', proyecto_id)

    user = request.user
    miembros = Miembro.objects.filter(proyecto=proyecto)
    usuario = Usuario.objects.get(user_id=user.id)

    miembro_aux = miembros.get(usuario=usuario, proyecto=proyecto)
    rol = miembro_aux.rol.get_queryset()
    if rol:
        permisos = obtener_permisos(rol)
    else:
        permisos = []

    context = {
        'form': form,
        'permisos': permisos,
        'proyecto_id': proyecto_id,
        'proyecto': proyecto
    }
    return render(request, 'roles/crear_rol.html', context)


@login_required
def modificar_rol(request, rol_id, proyecto_id):
    """
    Clase de la vista para la modificacion de un Rol
    """
    proyecto = Proyecto.objects.get(id=proyecto_id)
    rol = get_object_or_404(Rol, pk=rol_id)
    form = RolForm(instance=rol)

    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            form.save()
            return redirect('roles:index', proyecto_id)

    user = request.user
    miembros = Miembro.objects.filter(proyecto=proyecto)
    usuario = Usuario.objects.get(user_id=user.id)

    miembro_aux = miembros.get(usuario=usuario, proyecto=proyecto)
    rol = miembro_aux.rol.get_queryset()
    if rol:
        permisos = obtener_permisos(rol)
    else:
        permisos = []

    context = {
        'form': form,
        'permisos': permisos,
        'proyecto_id': proyecto_id,
        'proyecto': proyecto
    }
    return render(request, 'roles/modificar_rol.html', context)


@login_required
def eliminar_rol(request, rol_id, proyecto_id):
    """Clase de la vista para eliminar un rol"""
    proyecto = Proyecto.objects.get(id=proyecto_id)
    user = request.user
    miembros = Miembro.objects.filter(proyecto=proyecto)
    usuario = Usuario.objects.get(user_id=user.id)

    miembro_aux = miembros.get(usuario=usuario, proyecto=proyecto)
    rol = miembro_aux.rol.get_queryset()
    if rol:
        permisos = obtener_permisos(rol)
    else:
        permisos = []

    rol = get_object_or_404(Rol, pk=rol_id)
    if request.method == 'POST':
        rol.delete()
        return redirect('roles:index', proyecto_id)

    context = {
        'rol': rol,
        'permisos': permisos,
        'proyecto_id': proyecto_id,
        'proyecto': proyecto
    }
    return render(request, 'roles/eliminar_rol.html', context)


@login_required
def permiso_index(request):
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


@login_required
def crear_permiso(request):
    """
    Clase de la vista para la creacion de un nuevo Permiso.
    """

    if 2==2:
        messages.success(request, "El código del producto debe tener 5 carácteres")
    form = PermisoForm()
    if request.method == 'POST':
        form = PermisoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/roles/permissions/')

    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    p = obtener_permisos(rol)

    context = {
        'form': form,
        'permisos': p
    }
    return render(request, 'roles/permiso_form.html', context)