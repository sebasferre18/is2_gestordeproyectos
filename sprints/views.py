from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from funciones import obtener_permisos, obtener_permisos_usuario

# Create your views here.
from sprints.forms import AsignarUsForm
from proyectos.models import Proyecto, Miembro
from userstory.models import UserStory
from usuarios.models import Usuario
from .forms import SprintForm, DesarrolladorForm
from .models import Sprint, Desarrollador


@login_required
def index(request, proyecto_id):
    """
    Clase de la vista de la lista de Sprints
    """
    sprints = Sprint.objects.all().filter(proyecto_id=proyecto_id).order_by('-id')

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Visualizar Sprints" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    proyecto = Proyecto.objects.get(id=proyecto_id)

    try:
        estado = sprints.latest('id').estado
    except Sprint.DoesNotExist:
        estado = ""

    context = {
        'sprints': sprints,
        'permisos': permisos,
        'proyecto': proyecto,
        'estado': estado
    }

    return render(request, 'sprints/listar_sprints.html', context)


@login_required
def ver_detalles(request, sprint_id, proyecto_id):
    """
    Clase de la vista para la visualizacion de los detalles especificos de un sprint
    """
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    miembros = Miembro.objects.filter(proyecto=proyecto).order_by('id')

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Visualizar Sprints" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    context = {
        'proyecto': proyecto,
        'miembros': miembros,
        'permisos': permisos,
        'sprint': sprint,
    }
    return render(request, 'sprints/sprint_detalles.html', context)


@login_required
def crear_sprint(request, proyecto_id):
    """
    Clase de la vista para la creacion de un nuevo Sprint.
    """
    proyecto = Proyecto.objects.get(id=proyecto_id)
    form = SprintForm()
    if request.method == 'POST':
        form = SprintForm(request.POST)
        if form.is_valid():
            aux = form.save(commit=False)
            aux.proyecto = proyecto
            aux.save()
            return redirect('sprints:index', proyecto_id)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Crear Sprint" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    try:
        sprints = Sprint.objects.filter(proyecto_id=proyecto_id).order_by('id').latest('id')
        estado = sprints.estado
    except Sprint.DoesNotExist:
        estado = ""

    context = {
        'form': form,
        'permisos': permisos,
        'proyecto': proyecto,
        'estado': estado
    }
    return render(request, 'sprints/crear_sprint.html', context)

@login_required
def sprint_backlog(request, sprint_id, proyecto_id):
    """
        Clase de la vista para la visualizacion del Sprint Backlog
    """
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    us = UserStory.objects.all().filter(proyecto_id=proyecto_id, sprint_id=sprint_id).order_by('-prioridad')

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Visualizar Sprint Backlog" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    tiempo_restante = sprint.capacidad
    for u in us:
        tiempo_restante -= u.horas_estimadas

    context = {
        'proyecto': proyecto,
        'permisos': permisos,
        'sprint': sprint,
        'UserStory': us,
        'tiempo_restante': tiempo_restante
    }
    return render(request, 'sprints/sprint_backlog.html', context)


@login_required
def agregar_us(request, sprint_id, proyecto_id):
    """
        Clase de la vista para la visualizacion de User Stories a agregar en el Sprint Backlog
    """
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    us = UserStory.objects.all().filter(proyecto_id=proyecto_id, aprobado=False).exclude(sprint_id=sprint_id).order_by('-prioridad')
    sb = UserStory.objects.all().filter(proyecto_id=proyecto_id, sprint_id=sprint_id).order_by('-prioridad')

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Agregar US Al Sprint Backlog" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    tiempo_restante = sprint.capacidad
    for u in sb:
        tiempo_restante -= u.horas_estimadas

    context = {
        'proyecto': proyecto,
        'permisos': permisos,
        'sprint': sprint,
        'UserStory': us,
        'tiempo_restante': tiempo_restante
    }
    return render(request, 'sprints/agregar_us.html', context)

@login_required
def agregar_us_sprintbacklog(request, sprint_id, proyecto_id, us_id):
    """
        Clase de la vista para agregar el User Story al Sprint Backlog
    """
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    us = get_object_or_404(UserStory, pk=us_id)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Agregar US Al Sprint Backlog" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    us.sprint = sprint
    us.save()
    return redirect('sprints:agregar_us', sprint_id, proyecto_id)

@login_required
def quitar_us(request, sprint_id, proyecto_id, us_id):
    """
        Clase de la vista para quitar el User Story del Sprint Backlog
    """
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    us = get_object_or_404(UserStory, pk=us_id)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Quitar US Del Sprint Backlog" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    us.sprint = None
    us.save()
    return redirect('sprints:sprint_backlog', sprint_id, proyecto_id)


@login_required
def aprobar_us(request, sprint_id, proyecto_id, us_id):
    """
        Clase de la vista para la aprobacion de un User Story
    """
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    us = get_object_or_404(UserStory, pk=us_id)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Aprobar US" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    us.aprobado = True
    us.save()
    return redirect('sprints:sprint_backlog', sprint_id, proyecto_id)

@login_required
def iniciar_sprint(request, sprint_id, proyecto_id):
    """
    Clase de la vista para la inicializacion de un sprint
    """
    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Iniciar Sprint" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    sprint = get_object_or_404(Sprint, pk=sprint_id)
    sprint.estado = 'En ejecucion'
    sprint.fecha_inicio = date.today()
    sprint.save()

    return redirect('sprints:ver_detalles', sprint_id, proyecto_id)


@login_required
def finalizar_sprint(request, sprint_id, proyecto_id):
    """
    Clase de la vista para la finalizacion de un sprint
    """
    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Finalizar Sprint" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    sprint = get_object_or_404(Sprint, pk=sprint_id)
    sprint.estado = 'Finalizado'
    sprint.fecha_fin = date.today()
    sprint.save()

    us_sinaprobar = UserStory.objects.all().filter(proyecto_id=proyecto_id, sprint_id=sprint_id).exclude(aprobado=True)
    for us in us_sinaprobar:
        us.sprint = None
        us.sprint_previo = 3
        us.prioridad = (0.6 * us.business_value + 0.4 * us.user_point) + us.sprint_previo
        us.save()

    miembros = Miembro.objects.all()
    for m in miembros:
        m.userstory.clear()

    return redirect('sprints:ver_detalles', sprint_id, proyecto_id)


@login_required
def cancelar_sprint(request, sprint_id, proyecto_id):
    """
    Clase de la vista para la cancelacion de un sprint
    """
    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Cancelar Sprint" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    sprint = get_object_or_404(Sprint, pk=sprint_id)
    sprint.estado = 'Cancelado'
    sprint.fecha_fin = date.today()
    sprint.save()

    us_sinaprobar = UserStory.objects.all().filter(proyecto_id=proyecto_id, sprint_id=sprint_id).exclude(aprobado=True)
    for us in us_sinaprobar:
        us.sprint = None
        us.sprint_previo = 3
        us.prioridad = (0.6 * us.business_value + 0.4 * us.user_point) + us.sprint_previo
        us.save()

    miembros = Miembro.objects.all()
    for m in miembros:
        m.userstory.clear()

    return redirect('sprints:ver_detalles', sprint_id, proyecto_id)


@login_required
def listar_desarrolladores(request, sprint_id, proyecto_id):
    """
    Clase de la vista de la lista de Desarrolladores en un Sprint
    """
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    desarrolladores = Desarrollador.objects.filter(miembro__proyecto=proyecto).order_by('id')

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    context = {
        'proyecto': proyecto,
        'desarrolladores': desarrolladores,
        'permisos': permisos,
        'sprint': sprint,
    }
    return render(request, 'sprints/listar_desarrolladores.html', context)


@login_required
def asignar_us(request, sprint_id, proyecto_id, desarrollador_id):
    """
        Clase de la vista para la confirmacion de la asignacion de User Stories a los desarrolladores
    """
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    desarrollador = Desarrollador.objects.get(id=desarrollador_id)
    form = AsignarUsForm(instance=desarrollador, sprint_id=sprint_id)

    if request.method == 'POST':
        form = AsignarUsForm(request.POST, instance=desarrollador, sprint_id=sprint_id)
        if form.is_valid():
            form.save()
            return redirect('sprints:listar_desarrolladores', sprint_id, proyecto_id)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Asignar US A Usuario" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    context = {
        'form': form,
        'permisos': permisos,
        'desarrollador': desarrollador,
        'proyecto': proyecto,
        'sprint': sprint,
    }
    return render(request, 'sprints/confirm_asignar_us.html', context)

@login_required
def asignar_desarrolladores(request, sprint_id, proyecto_id):
    """
    Clase de la vista para la asignacion de desarrolladores en un Sprint
    """
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    desarrolladores = Desarrollador.objects.filter(sprint=sprint)
    ids = []

    for a in desarrolladores:
        ids.append(a.miembro.usuario.user_id)

    miembros = Miembro.objects.filter(proyecto=proyecto).exclude(usuario__user_id__in=ids).order_by('id')

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    context = {
        'miembros': miembros,
        'permisos': permisos,
        'proyecto': proyecto,
        'sprint': sprint,
    }
    return render(request, "sprints/asignar_desarrolladores.html", context)


@login_required
def asignar_capacidad_por_dia(request, sprint_id, proyecto_id, miembro_id):
    """
    Clase de la vista para la asignacion de desarrolladores en un Sprint
    """
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    miembro = Miembro.objects.get(id=miembro_id)
    form = DesarrolladorForm()

    if request.method == 'POST':
        form = DesarrolladorForm(request.POST)
        if form.is_valid():
            aux = form.save(commit=False)
            aux.miembro = miembro
            aux.sprint = sprint
            aux.capacidad_total = aux.capacidad_por_dia * sprint.duracion
            aux.save()
            sprint.capacidad += aux.capacidad_total
            sprint.save()
            return redirect('sprints:asignar_desarrolladores', sprint_id, proyecto_id)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    context = {
        'miembro': miembro,
        'permisos': permisos,
        'proyecto': proyecto,
        'sprint': sprint,
        'form': form
    }
    return render(request, "sprints/asignar_capacidad_por_dia.html", context)

