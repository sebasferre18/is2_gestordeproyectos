from datetime import datetime

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario
from .models import Rol, Permiso
from .forms import RolForm, PermisoForm
from proyectos.models import Proyecto, Miembro, Historial, Notificacion
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

    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1
    context = {
        'role_list': roles,
        'permisos': permisos,
        'proyecto_id': proyecto_id,
        'proyecto': proyecto,
        'cantidad': cantidad
    }
    return render(request, 'roles/index.html', context)


@login_required
def crear_rol(request, proyecto_id):
    """
    Clase de la vista para la creacion de un nuevo Rol.
    """
    proyecto = Proyecto.objects.get(id=proyecto_id)
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)

    form = RolForm()
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            perm = recolectar_permisos(form.cleaned_data['permiso'])

            aux = form.save(commit=False)
            aux.proyecto = proyecto
            aux.save()
            form.save_m2m()

            informacion = "ID: " + str(aux.id) + "; Nombre: " + aux.nombre + "; Descripcion: " + aux.descripcion + \
                          "; Permisos: " + perm
            historial = Historial(proyecto=proyecto, responsable=usuario, fecha=datetime.now(), accion='Creacion',
                                  elemento='Roles', informacion=informacion)
            historial.save()
            return redirect('roles:index', proyecto_id)

    miembros = Miembro.objects.filter(proyecto=proyecto)
    miembro_aux = miembros.get(usuario=usuario, proyecto=proyecto)
    rol = miembro_aux.rol.get_queryset()
    if rol:
        permisos = obtener_permisos(rol)
    else:
        permisos = []

    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1
    context = {
        'form': form,
        'permisos': permisos,
        'proyecto_id': proyecto_id,
        'proyecto': proyecto,
        'cantidad': cantidad
    }
    return render(request, 'roles/crear_rol.html', context)


@login_required
def modificar_rol(request, rol_id, proyecto_id):
    """
    Clase de la vista para la modificacion de un Rol
    """
    proyecto = Proyecto.objects.get(id=proyecto_id)
    rol = get_object_or_404(Rol, pk=rol_id)
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)

    form = RolForm(instance=rol)
    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            perm = recolectar_permisos(form.cleaned_data['permiso'])
            informacion = "ID: " + str(rol_id) + "; Nombre: " + form.cleaned_data['nombre'] + "; Descripcion: " + \
                          form.cleaned_data['descripcion'] + "; Permisos: " + perm

            form.save()

            historial = Historial(proyecto=proyecto, responsable=usuario, fecha=datetime.now(), accion='Modificacion',
                                  elemento='Roles', informacion=informacion)
            historial.save()
            return redirect('roles:index', proyecto_id)

    miembros = Miembro.objects.filter(proyecto=proyecto)
    miembro_aux = miembros.get(usuario=usuario, proyecto=proyecto)
    rol = miembro_aux.rol.get_queryset()
    if rol:
        permisos = obtener_permisos(rol)
    else:
        permisos = []

    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1
    context = {
        'form': form,
        'permisos': permisos,
        'proyecto_id': proyecto_id,
        'proyecto': proyecto,
        'cantidad': cantidad
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
        perm = recolectar_permisos(rol.permiso.get_queryset())
        informacion = "ID: " + str(rol_id) + "; Nombre: " + rol.nombre + "; Descripcion: " + \
                      rol.descripcion + "; Permisos: " + perm

        rol.delete()
        historial = Historial(proyecto=proyecto, responsable=usuario, fecha=datetime.now(), accion='Eliminacion',
                              elemento='Roles', informacion=informacion)
        historial.save()
        return redirect('roles:index', proyecto_id)

    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1
    context = {
        'rol': rol,
        'permisos': permisos,
        'proyecto_id': proyecto_id,
        'proyecto': proyecto,
        'cantidad': cantidad
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

    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1
    context = {
        'permiso_list': permisos,
        'permisos': p,
        'cantidad': cantidad
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

    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1
    context = {
        'form': form,
        'permisos': p,
        'cantidad': cantidad
    }
    return render(request, 'roles/permiso_form.html', context)


def recolectar_permisos(permisos):
    perm = ""
    if permisos:
        for i, p in enumerate(permisos, start=1):
            perm += p.nombre
            if i < len(permisos):
                perm += ", "
    else:
        perm = "No tiene permisos"

    return perm
