import json
from datetime import date, datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from funciones import obtener_permisos, obtener_permisos_usuario

# Create your views here.
from sprints.forms import AsignarUsForm
from proyectos.models import Proyecto, Miembro, Historial, Notificacion
from userstory.models import UserStory, Tarea, TareaAux
from usuarios.models import Usuario
from .forms import SprintForm, DesarrolladorForm
from .models import Sprint, Desarrollador

from django.contrib import messages


@login_required
def index(request, proyecto_id):
    """
    Clase de la vista de la lista de Sprints
    """
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
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

    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1
    context = {
        'sprints': sprints,
        'permisos': permisos,
        'proyecto': proyecto,
        'estado': estado,
        'cantidad': cantidad
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
    desarrolladores = Desarrollador.objects.filter(miembro__proyecto=proyecto, sprint=sprint)
    tareas = Tarea.objects.filter(userstory__sprint=sprint)
    sb = UserStory.objects.all().filter(proyecto_id=proyecto_id, sprint_id=sprint_id)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Visualizar Sprints" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    capacidad_trabajo = 0
    for d in desarrolladores:
        capacidad_trabajo += d.capacidad_total

    capacidad_trabajo_restante = capacidad_trabajo
    for t in tareas:
        capacidad_trabajo_restante -= t.horas_trabajadas

    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1
    context = {
        'proyecto': proyecto,
        'miembros': miembros,
        'permisos': permisos,
        'sprint': sprint,
        'capacidad_trabajo': capacidad_trabajo,
        'capacidad_trabajo_restante': capacidad_trabajo_restante,
        'cantidad': cantidad
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
            aux.capacidad = 0
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

    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1
    context = {
        'form': form,
        'permisos': permisos,
        'proyecto': proyecto,
        'estado': estado,
        'cantidad': cantidad
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
    tareas = Tarea.objects.filter(userstory__sprint=sprint)
    desarrolladores = Desarrollador.objects.filter(miembro__proyecto=proyecto, sprint=sprint)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Visualizar Sprint Backlog" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    tiempo_restante = sprint.capacidad
    for u in us:
        tiempo_restante -= u.horas_estimadas

    capacidad_restante = 0
    for d in desarrolladores:
        capacidad_restante += d.capacidad_total

    for t in tareas:
        capacidad_restante -= t.horas_trabajadas

    if tiempo_restante < 0:
        messages.warning(request, "Se sobrepaso la capacidad de trabajo.")

    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1

    context = {
        'proyecto': proyecto,
        'permisos': permisos,
        'sprint': sprint,
        'UserStory': us,
        'tiempo_restante': tiempo_restante,
        'capacidad_restante': capacidad_restante,
        'cantidad': cantidad
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

    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1
    context = {
        'proyecto': proyecto,
        'permisos': permisos,
        'sprint': sprint,
        'UserStory': us,
        'tiempo_restante': tiempo_restante,
        'cantidad': cantidad
    }
    return render(request, 'sprints/agregar_us.html', context)

@login_required
def agregar_us_sprintbacklog(request, sprint_id, proyecto_id, us_id):
    """
        Clase de la vista para agregar el User Story al Sprint Backlog
    """
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
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

    informacion = "Se ha agregado el User Story: '" + us.nombre + "' al Sprint Backlog del sprint '" + \
                  sprint.nombre + "'"
    historial = Historial(proyecto=proyecto, responsable=usuario, fecha=datetime.now(), accion='Modificacion',
                          elemento='Sprints', informacion=informacion)
    historial.save()
    return redirect('sprints:agregar_us', sprint_id, proyecto_id)

@login_required
def quitar_us(request, sprint_id, proyecto_id, us_id):
    """
        Clase de la vista para quitar el User Story del Sprint Backlog
    """
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
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

    informacion = "Se ha quitado el User Story: '" + us.nombre + "' del Sprint Backlog del sprint '" + \
                  sprint.nombre + "'"
    historial = Historial(proyecto=proyecto, responsable=usuario, fecha=datetime.now(), accion='Modificacion',
                          elemento='Sprints', informacion=informacion)
    historial.save()
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
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    desarrolladores = Desarrollador.objects.filter(miembro__proyecto=proyecto, sprint_id=sprint_id)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Iniciar Sprint" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    sprint = get_object_or_404(Sprint, pk=sprint_id)
    sprint.estado = 'En ejecucion'
    sprint.fecha_inicio = date.today()

    sb = UserStory.objects.all().filter(proyecto_id=proyecto_id, sprint_id=sprint_id)
    horas_sb = 0

    for u in sb:
        tareas = Tarea.objects.filter(userstory=u)
        for t in tareas:
            horas_sb -= t.horas_trabajadas
        horas_sb += u.horas_estimadas

    sprint.story_points_iniciales = horas_sb
    sprint.save()

    informacion = "El sprint '" + sprint.nombre + "' fue iniciado"
    historial = Historial(proyecto=proyecto, responsable=usuario, fecha=datetime.now(), accion='Modificacion',
                          elemento='Sprints', informacion=informacion)
    historial.save()

    for m in desarrolladores:
        informacion = "El sprint '" + sprint.nombre + "' del proyecto '" + proyecto.nombre + \
                      "' fue iniciado"
        notificacion = Notificacion(fecha=datetime.now(), informacion=informacion, destinatario=m.miembro.usuario, visto=False)
        notificacion.save()
    return redirect('sprints:ver_detalles', sprint_id, proyecto_id)


@login_required
def finalizar_sprint(request, sprint_id, proyecto_id):
    """
    Clase de la vista para la finalizacion de un sprint
    """
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    desarrolladores = Desarrollador.objects.filter(miembro__proyecto=proyecto, sprint_id=sprint_id)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Finalizar Sprint" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    sprint = get_object_or_404(Sprint, pk=sprint_id)
    sprint.estado = 'Finalizado'
    sprint.fecha_fin = date.today()

    userstories = UserStory.objects.filter(proyecto_id=proyecto_id)

    story_points_totales = 0
    for u in userstories:
        story_points_totales += u.horas_estimadas

    us_aprobados = UserStory.objects.all().filter(proyecto_id=proyecto_id, sprint_id=sprint_id, aprobado=True)
    horas_aprobadas = 0

    for u in us_aprobados:
        horas_aprobadas += u.horas_estimadas

    sprint.horas_aprobadas += horas_aprobadas
    story_points_totales -= horas_aprobadas
    sprints_finalizados = Sprint.objects.filter(proyecto_id=proyecto_id, estado='Finalizado').exclude(id=sprint_id)

    for s in sprints_finalizados:
        story_points_totales -= s.horas_aprobadas

    us_sinaprobar = UserStory.objects.all().filter(proyecto_id=proyecto_id, sprint_id=sprint_id).exclude(aprobado=True)
    for us in us_sinaprobar:
        tarea = Tarea.objects.filter(userstory=us)
        for t in tarea:
            tarea_aux = TareaAux(sprint=sprint, fecha=t.fecha, horas_trabajadas=t.horas_trabajadas)
            tarea_aux.save()
        us.sprint = None
        us.sprint_previo = 3
        us.prioridad = (0.6 * us.business_value + 0.4 * us.user_point) + us.sprint_previo
        us.save()

    sprint.story_points = story_points_totales
    sprint.save()

    miembros = Miembro.objects.all()
    for m in miembros:
        m.userstory.clear()

    informacion = "El sprint '" + sprint.nombre + "' fue finalizado"
    historial = Historial(proyecto=proyecto, responsable=usuario, fecha=datetime.now(), accion='Modificacion',
                          elemento='Sprints', informacion=informacion)
    historial.save()

    for m in desarrolladores:
        informacion = "El sprint '" + sprint.nombre + "' del proyecto '" + proyecto.nombre + \
                      "' fue finalizado"
        notificacion = Notificacion(fecha=datetime.now(), informacion=informacion, destinatario=m.miembro.usuario, visto=False)
        notificacion.save()
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
    desarrolladores = Desarrollador.objects.filter(miembro__proyecto=proyecto, sprint=sprint).order_by('id')

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    capacidad_trabajo = 0
    for d in desarrolladores:
        capacidad_trabajo += d.capacidad_total

    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1
    context = {
        'proyecto': proyecto,
        'desarrolladores': desarrolladores,
        'permisos': permisos,
        'sprint': sprint,
        'capacidad_trabajo': capacidad_trabajo,
        'cantidad': cantidad
    }
    return render(request, 'sprints/listar_desarrolladores.html', context)


@login_required
def asignar_us(request, sprint_id, proyecto_id, desarrollador_id):
    """
        Clase de la vista para la confirmacion de la asignacion de User Stories a los desarrolladores
    """
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    desarrollador = Desarrollador.objects.get(id=desarrollador_id)
    form = AsignarUsForm(instance=desarrollador, sprint_id=sprint_id)

    if request.method == 'POST':
        form = AsignarUsForm(request.POST, instance=desarrollador, sprint_id=sprint_id)
        if form.is_valid():
            us = recolectar_us(form.cleaned_data['userstory'])
            form.save()

            if form.cleaned_data['userstory']:
                informacion = "Al desarrollador '" + desarrollador.miembro.usuario.user.username + "' del sprint '" + \
                              sprint.nombre + "' se le fue asignado los siguientes US: " + us
            else:
                informacion = "El desarrollador '" + desarrollador.miembro.usuario.user.username + "' del sprint '" + \
                              sprint.nombre + "' ya no tiene US asignados"
            historial = Historial(proyecto=proyecto, responsable=usuario, fecha=datetime.now(), accion='Modificacion',
                                  elemento='Sprints', informacion=informacion)
            historial.save()

            if form.cleaned_data['userstory']:
                informacion = proyecto.nombre + ": Del sprint '" + \
                              sprint.nombre + "' le fueron asignados los siguientes US: " + us
            else:
                informacion = proyecto.nombre + ": Del sprint '" + \
                              sprint.nombre + "' ya no tienes US asignados"

            notificacion = Notificacion(fecha=datetime.now(), informacion=informacion,
                                        destinatario=desarrollador.miembro.usuario, visto=False)
            notificacion.save()
            return redirect('sprints:listar_desarrolladores', sprint_id, proyecto_id)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Asignar US A Usuario" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1
    context = {
        'form': form,
        'permisos': permisos,
        'desarrollador': desarrollador,
        'proyecto': proyecto,
        'sprint': sprint,
        'cantidad': cantidad
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

    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1
    context = {
        'miembros': miembros,
        'permisos': permisos,
        'proyecto': proyecto,
        'sprint': sprint,
        'cantidad': cantidad
    }
    return render(request, "sprints/asignar_desarrolladores.html", context)


@login_required
def asignar_capacidad_por_dia(request, sprint_id, proyecto_id, miembro_id):
    """
    Clase de la vista para la asignacion de desarrolladores en un Sprint
    """
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
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

            informacion = "El miembro '" + miembro.usuario.user.username + \
                          "' fue asignado como Desarrollador en el sprint '" + sprint.nombre + \
                          "' con una capacidad por dia de " + str(aux.capacidad_por_dia) + " horas"
            historial = Historial(proyecto=proyecto, responsable=usuario, fecha=datetime.now(), accion='Modificacion',
                                  elemento='Sprints', informacion=informacion)
            historial.save()

            informacion = proyecto.nombre + ": usted fue asignado como Desarrollador en el Sprint '" + sprint.nombre + "' con capacidad por dia de " + str(aux.capacidad_por_dia) + " horas"
            notificacion = Notificacion(fecha=datetime.now(), informacion=informacion,
                                        destinatario=aux.miembro.usuario, visto=False)
            notificacion.save()
            return redirect('sprints:asignar_desarrolladores', sprint_id, proyecto_id)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1
    context = {
        'miembro': miembro,
        'permisos': permisos,
        'proyecto': proyecto,
        'sprint': sprint,
        'form': form,
        'cantidad': cantidad
    }
    return render(request, "sprints/asignar_capacidad_por_dia.html", context)

@login_required
def modificar_capacidad_dia(request, sprint_id, proyecto_id, desarrollador_id):
    """
    Clase de la vista para la modificacion de la capacidad de horas por dia de los desarrolladores en un Sprint
    """
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    miembro = Desarrollador.objects.get(id=desarrollador_id)
    form = DesarrolladorForm(instance=miembro)

    if request.method == 'POST':
        form = DesarrolladorForm(request.POST, instance=miembro)
        if form.is_valid():
            aux = form.save(commit=False)
            sprint.capacidad -= aux.capacidad_total
            aux.capacidad_total = aux.capacidad_por_dia * sprint.duracion
            aux.save()
            sprint.capacidad += aux.capacidad_total
            sprint.save()

            informacion = "La capacidad por dia del Desarrollador '" + miembro.miembro.usuario.user.username + \
                          "' del sprint '" + sprint.nombre + "' ahora es de " + str(aux.capacidad_por_dia) + " horas"
            historial = Historial(proyecto=proyecto, responsable=usuario, fecha=datetime.now(), accion='Modificacion',
                                  elemento='Sprints', informacion=informacion)
            historial.save()

            informacion = proyecto.nombre + ": en el sprint '" + sprint.nombre + "' su capacidad por dia ahora es de " + str(aux.capacidad_por_dia) + " horas"
            notificacion = Notificacion(fecha=datetime.now(), informacion=informacion,
                                        destinatario=aux.miembro.usuario, visto=False)
            notificacion.save()
            return redirect('sprints:listar_desarrolladores', sprint_id, proyecto_id)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Desarrollador.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1
    context = {
        'miembro': miembro,
        'permisos': permisos,
        'proyecto': proyecto,
        'sprint': sprint,
        'form': form,
        'cantidad': cantidad
    }
    return render(request, "sprints/modificar_capacidad_dia.html", context)

@login_required
def acceso_denegado(request, sprint_id, proyecto_id):
    """
    Clase de la vista de acceso denegado a un sprint
    """
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1
    context = {
        'sprint_id': sprint_id,
        'proyecto_id': proyecto_id,
        'cantidad': cantidad
    }
    return render(request, 'sprints/acceso_denegado.html', context)

@login_required
def burndown_chart(request, proyecto_id):
    """
        Clase de la vista del Burndown Chart de los sprints
    """
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    sprints = Sprint.objects.filter(proyecto=proyecto, estado='Finalizado').order_by('id')

    x_data = [" "]
    y_data = [proyecto.story_points]

    for i, s in enumerate(sprints, start=1):
        x_data.append(s.nombre)
        y_data.append(s.story_points)

    x_data.append(" ")

    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1
    context = {
        'proyecto': proyecto,
        'x_data': json.dumps(x_data),
        'y_data': y_data,
        'cantidad': cantidad
    }
    return render(request, 'sprints/burndown_chart.html', context)


@login_required
def burndown_chart_redux(request, sprint_id, proyecto_id):
    """
        Clase de la vista del Burndown Chart de un Sprint
    """
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    sprint = Sprint.objects.get(id=sprint_id)
    sb = UserStory.objects.all().filter(proyecto_id=proyecto_id, sprint_id=sprint_id)

    x_data = [" "]
    y_data = [sprint.story_points_iniciales]
    y_data_ideal = []
    horas_totales_sprint = y_data[0]
    horas_ideales_dia = horas_totales_sprint / sprint.duracion
    horas_quemadas = 0

    i = 0
    j = 0
    while i - j < sprint.duracion:
        dia = sprint.fecha_inicio + timedelta(days=i)
        if dia.isoweekday() == 6 or dia.isoweekday() == 7:
            i += 1
            j += 1
        else:
            x_data.append(str(dia.strftime("%d-%m-%Y")))
            y_data_ideal.append(round(horas_totales_sprint - (horas_ideales_dia * (i-j))))
            for u in sb:
                tareas = Tarea.objects.filter(userstory=u, fecha__day=dia.day, fecha__month=dia.month, fecha__year=dia.year)
                for t in tareas:
                    horas_quemadas += t.horas_trabajadas
            tarea_aux = TareaAux.objects.filter(sprint=sprint, fecha__day=dia.day, fecha__month=dia.month, fecha__year=dia.year)
            for ta in tarea_aux:
                horas_quemadas += ta.horas_trabajadas
            if datetime.now().date() >= dia:
                y_data.append(horas_totales_sprint - horas_quemadas)
            i += 1

    print(horas_quemadas)
    x_data.append(" ")
    y_data_ideal.append(0)

    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1
    context = {
        'proyecto': proyecto,
        'sprint': sprint,
        'x_data': json.dumps(x_data),
        'y_data': y_data,
        'y_data_ideal': y_data_ideal,
        'cantidad': cantidad
    }
    return render(request, 'sprints/burndown_chart_redux.html', context)

def recolectar_us(usquery):
    us = ""
    if usquery:
        for i, p in enumerate(usquery, start=1):
            us += p.nombre
            if i < len(usquery):
                us += ", "
    else:
        us = "No tiene US asignado"

    return us
