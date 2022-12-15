from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import date, datetime

from proyectos.models import Proyecto, Miembro, Historial
from proyectos.forms import ProyectoForm, MiembroForm, MiembroFormSet
from userstory.models import UserStory
from usuarios.models import Usuario
from roles.models import Rol, Permiso
from funciones import obtener_permisos

from userstory import views

"""
Vistas de la app de Proyectos.
"""
permisos_sm = [
    'Visualizar Roles',
    'Crear Rol',
    'Modificar Rol',
    'Eliminar Rol',
    'Iniciar Proyecto',
    'Finalizar Proyecto',
    'Cancelar Proyecto',
    'Asignar Miembros',
    'Desasignar Miembros',
    'Gestionar Roles De Un Usuario',
    'Visualizar US',
    'Modificar US',
    'Crear US',
    'Visualizar Tipo US',
    'Crear Tipo US',
    'Modificar Tipo US',
    'Eliminar Tipo US',
    'Importar Tipo US',
    'Visualizar Sprints',
    'Crear Sprint',
    'Visualizar Sprint Backlog',
    'Agregar US Al Sprint Backlog',
    'Quitar US Del Sprint Backlog',
    'Aprobar US',
    'Visualizar Tablero',
    'Asignar US A Usuario',
    'Asignar Desarrolladores',
    'Iniciar Sprint',
    'Finalizar Sprint',
    'Cancelar Sprint',
    'Adjuntar Notas'
]

permisos_de = [
    'Visualizar Roles',
    'Visualizar US',
    'Modificar US',
    'Crear US',
    'Visualizar Tipo US',
    'Crear Tipo US',
    'Modificar Tipo US',
    'Eliminar Tipo US',
    'Importar Tipo US',
    'Visualizar Sprints',
    'Visualizar Sprint Backlog',
    'Visualizar Tablero'
]

@login_required
def listar_proyectos(request):
    """
    Clase de la vista de la lista de Proyectos
    """
    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    if "Crear Permiso" in permisos:
        proyecto = Proyecto.objects.all().order_by('id')
    else:
        proyecto = Proyecto.objects.filter(miembro__usuario__user=request.user).order_by('id')

    contexto = {'proyectos': proyecto, 'permisos': permisos}
    return render(request, 'proyectos/proyectos_list.html', contexto)


@login_required
def crear_proyecto(request):
    """
    Clase de la vista para la creacion de un nuevo proyecto
    """
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    miembro = Miembro()
    miembro.usuario = usuario

    rol = usuario.rol.all()
    permisos = obtener_permisos(rol)

    if request.method == 'POST':
        perm_sm = Permiso.objects.filter(nombre__in=permisos_sm)
        perm_de = Permiso.objects.filter(nombre__in=permisos_de)
        formulario = ProyectoForm(request.POST)
        formulario_miembro = MiembroFormSet(request.POST)
        if formulario.is_valid() and formulario_miembro.is_valid():
            form = formulario.save()

            sm = Rol(nombre="Scrum Master", descripcion="Rol de Scrum Master", proyecto=form)
            sm.save()
            sm.permiso.set(perm_sm)
            de = Rol(nombre="Developer", descripcion="Rol de Developer", proyecto=form)
            de.save()
            de.permiso.set(perm_de)

            for a in formulario_miembro.forms:
                up = a.save(commit=False)
                up.proyecto = form
                up.save()
                up.rol.set([sm])
            return HttpResponseRedirect('/proyectos/')
    else:
        formulario = ProyectoForm()
        formulario_miembro = MiembroFormSet()
    return render(request, 'proyectos/crear_proyecto.html', {'formulario':formulario, 'formulario_miembro':formulario_miembro, 'permisos':permisos})


@login_required
def asignar_usuarios(request, proyecto_id):
    """
    Clase de la vista para la asignacion de miembros en un proyecto
    """
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    miembros = Miembro.objects.filter(proyecto=proyecto)
    ids = []

    for a in miembros:
        ids.append(a.usuario.user_id)

    usuarios = Usuario.objects.exclude(user_id__in=ids)

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
        'usuarios': usuarios,
        'permisos': permisos,
        'proyecto_id': proyecto_id,
        'proyecto': proyecto
    }
    return render(request, "proyectos/asignar_usuarios.html", context)

@login_required
def desasignar_usuarios(request, proyecto_id):
    """
    Clase de la vista para la desasignacion de miembros en un proyecto
    """
    user = request.user
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    miembros = Miembro.objects.filter(proyecto=proyecto).exclude(usuario__user=user)

    miembros_aux = Miembro.objects.filter(proyecto=proyecto)
    usuario = Usuario.objects.get(user_id=user.id)

    miembro_aux = miembros_aux.get(usuario=usuario, proyecto=proyecto)
    rol = miembro_aux.rol.get_queryset()
    if rol:
        permisos = obtener_permisos(rol)
    else:
        permisos = []

    context = {
        'miembros': miembros,
        'permisos': permisos,
        'proyecto_id': proyecto_id,
        'proyecto': proyecto
    }
    return render(request, 'proyectos/desasignar_usuarios.html', context)

@login_required
def gestionar_roles(request, proyecto_id, miembro_id):
    """
    Clase de la vista para la gestion de roles de un usuario
    """
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    miembro = Miembro.objects.get(id=miembro_id)
    form = MiembroForm(instance=miembro, pro_id=proyecto_id)

    if request.method == 'POST':
        form = MiembroForm(request.POST, instance=miembro, pro_id=proyecto_id)
        if form.is_valid():
            roles = recolectar_roles(form.cleaned_data['rol'])
            form.save()

            if form.cleaned_data['rol']:
                informacion = "Al miembro '" + miembro.usuario.user.username + \
                              "' se le fue asignado los siguientes roles: " + roles
            else:
                informacion = "El miembro '" + miembro.usuario.user.username + "' ya no tiene roles asignados"
            historial = Historial(proyecto=proyecto, responsable=usuario, fecha=datetime.now(), accion='Modificacion',
                                  elemento='Proyectos', informacion=informacion)
            historial.save()
            return redirect('proyectos:ver_detalles', proyecto_id)

    miembros = Miembro.objects.filter(proyecto=proyecto)

    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    if "Crear Proyecto" not in permisos:
        try:
            miembro_aux = miembros.get(usuario=usuario, proyecto=proyecto)
        except Miembro.DoesNotExist:
            return redirect('proyectos:acceso_denegado')
        rol = miembro_aux.rol.get_queryset()
        if rol:
            permisos = obtener_permisos(rol)
        else:
            permisos = []

    context = {
        'form': form,
        'permisos': permisos,
        'miembro': miembro,
        'proyecto_id': proyecto_id,
        'proyecto': proyecto,
    }
    return render(request, 'proyectos/gestionar_roles.html', context)

@login_required
def agregar_miembro(request, proyecto_id, user_id):
    """
    Clase de la vista para eliminar a un miembro de un proyecto
    """
    user = request.user
    usuario_aux = Usuario.objects.get(user_id=user.id)
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    usuario = get_object_or_404(Usuario, user_id=user_id)

    miembro = Miembro(proyecto=proyecto, usuario=usuario)
    miembro.save()

    informacion = "El usuario '" + usuario.user.username + \
                  "' fue asignado como Miembro de este proyecto"
    historial = Historial(proyecto=proyecto, responsable=usuario_aux, fecha=datetime.now(), accion='Modificacion',
                          elemento='Proyectos', informacion=informacion)
    historial.save()
    return redirect('proyectos:asignar_usuarios', proyecto_id)

@login_required
def eliminar_miembro(request, proyecto_id, miembro_id):
    """
    Clase de la vista para eliminar a un miembro de un proyecto
    """
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    miembro = get_object_or_404(Miembro, id=miembro_id)
    miembro.delete()

    informacion = "El usuario '" + miembro.usuario.user.username + \
                  "' fue desasignado como Miembro de este proyecto"
    historial = Historial(proyecto=proyecto, responsable=usuario, fecha=datetime.now(), accion='Modificacion',
                          elemento='Proyectos', informacion=informacion)
    historial.save()
    return redirect('proyectos:desasignar_usuarios', proyecto_id)


@login_required
def ver_detalles(request, proyecto_id):
    """
    Clase de la vista para la visualizacion de los detalles especificos de un proyecto
    """
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    miembros = Miembro.objects.filter(proyecto=proyecto).order_by('id')

    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    if "Crear Proyecto" not in permisos:
        try:
            miembro = miembros.get(usuario=usuario, proyecto=proyecto)
        except Miembro.DoesNotExist:
            return redirect('proyectos:acceso_denegado')
        rol = miembro.rol.get_queryset()
        if rol:
            permisos = obtener_permisos(rol)
        else:
            permisos = []

    context = {
        'proyecto': proyecto,
        'miembros': miembros,
        'permisos': permisos
    }
    return render(request, 'proyectos/proyecto_detalles.html', context)

@login_required
def iniciar_proyecto(request, proyecto_id):
    """
    Clase de la vista para la inicializacion de un proyecto
    """
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    proyecto.estado = 'En ejecucion'
    proyecto.fecha_inicio = date.today()

    userstories = UserStory.objects.filter(proyecto=proyecto)

    story_points_totales = 0
    for u in userstories:
        story_points_totales += u.horas_estimadas
    proyecto.story_points = story_points_totales
    proyecto.save()

    informacion = "El proyecto fue iniciado"
    historial = Historial(proyecto=proyecto, responsable=usuario, fecha=datetime.now(), accion='Modificacion',
                          elemento='Proyectos', informacion=informacion)
    historial.save()
    return redirect('proyectos:ver_detalles', proyecto_id)


@login_required
def finalizar_proyecto(request, proyecto_id):
    """
    Clase de la vista para la finalizacion de un proyecto
    """
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    proyecto.estado = 'Finalizado'
    proyecto.fecha_fin = date.today()
    proyecto.save()

    informacion = "El proyecto fue finalizado"
    historial = Historial(proyecto=proyecto, responsable=usuario, fecha=datetime.now(), accion='Modificacion',
                          elemento='Proyectos', informacion=informacion)
    historial.save()
    return redirect('proyectos:ver_detalles', proyecto_id)


@login_required
def cancelar_proyecto(request, proyecto_id):
    """
    Clase de la vista para la cancelacion de un proyecto
    """
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    proyecto.estado = 'Cancelado'
    proyecto.fecha_fin = date.today()
    proyecto.save()

    informacion = "El proyecto fue cancelado"
    historial = Historial(proyecto=proyecto, responsable=usuario, fecha=datetime.now(), accion='Modificacion',
                          elemento='Proyectos', informacion=informacion)
    historial.save()
    return redirect('proyectos:ver_detalles', proyecto_id)

@login_required
def acceso_denegado(request):
    """
    Clase de la vista de acceso denegado a un proyecto
    """
    return render(request, 'proyectos/acceso_denegado.html')

@login_required
def falta_de_permisos(request, proyecto_id):
    """
    Clase de la vista de acceso denegado generico por falta de permisos
    """
    context = {
        'proyecto_id': proyecto_id,
    }
    return render(request, 'proyectos/falta_de_permisos.html', context)

@login_required
def notificaciones(request):
    """
    Clase de la vista de las notificaciones de un Proyecto
    """
    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    context = {
        'permisos': permisos
    }
    return render(request, 'proyectos/notificaciones.html', context)

@login_required
def historial_modificaciones(request, proyecto_id):
    """
    Clase de la vista del historial de modificaciones de un proyecto
    """
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    historial = Historial.objects.filter(proyecto=proyecto).order_by('-fecha')

    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    context = {
        'proyecto': proyecto,
        'permisos': permisos,
        'historial': historial
    }
    return render(request, 'proyectos/historial_modificaciones.html', context)


def recolectar_roles(rolquery):
    roles = ""
    if rolquery:
        for i, p in enumerate(rolquery, start=1):
            roles += p.nombre
            if i < len(rolquery):
                roles += ", "
    else:
        roles = "No tiene roles asignados"

    return roles
