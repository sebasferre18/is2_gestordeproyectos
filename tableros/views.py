from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from datetime import datetime

from funciones import obtener_permisos_usuario
from proyectos.models import Proyecto, Miembro
from sprints.models import Sprint, Desarrollador
from tipo_us.models import MiembroTipoUs
from userstory.models import UserStory, Tarea, Nota
from .forms import ActualizarEstadoForm, TareaForm, NotaForm
from .models import Tablero


@login_required
def index(request, sprint_id, proyecto_id):
    """
        Clase de la vista de la lista de Tableros
    """
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    proyecto = Proyecto.objects.get(id=proyecto_id)

    tableros = Tablero.objects.filter(tipo_us__proyecto_id=proyecto_id).order_by('id')

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Visualizar Tablero" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    context = {
        'tableros': tableros,
        'permisos': permisos,
        'proyecto': proyecto,
        'sprint': sprint,
    }

    return render(request, 'tableros/listar_tableros.html', context)


@login_required
def tablero_detalles(request, tablero_id, sprint_id, proyecto_id):
    """
        Clase de la vista para la visualizacion de un tablero
    """
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    tablero = Tablero.objects.get(id=tablero_id)
    us = UserStory.objects.all().filter(proyecto_id=proyecto_id, sprint_id=sprint_id, tipo_us=tablero.tipo_us).order_by('-prioridad')

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    try:
        desarrollador = Desarrollador.objects.get(miembro__usuario__user=request.user, sprint=sprint)
    except Desarrollador.DoesNotExist:
        desarrollador = []

    if "Visualizar Tablero" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    campos = tablero.campos

    context = {
        'tablero': tablero,
        'permisos': permisos,
        'proyecto': proyecto,
        'sprint': sprint,
        'campos': campos.split(','),
        'desarrollador': desarrollador,
        'us': us
    }
    return render(request, 'tableros/tablero_detalles.html', context)


@login_required
def tablero_us_detalles(request, tablero_id, sprint_id, proyecto_id, us_id):
    """
        Clase de la vista para la visualizacion de un US en el tablero
    """
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    tablero = Tablero.objects.get(id=tablero_id)
    us = UserStory.objects.get(id=us_id)
    tareas = Tarea.objects.filter(userstory=us)
    notas = Nota.objects.filter(userstory=us)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    try:
        desarrollador = Desarrollador.objects.get(miembro__usuario__user=request.user, sprint=sprint)
    except Desarrollador.DoesNotExist:
        desarrollador = []

    if "Visualizar Tablero" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    horas_restantes = us.horas_estimadas
    for t in tareas:
        horas_restantes -= t.horas_trabajadas

    tareas_desarrollador_dia = Tarea.objects.filter(creador=desarrollador.miembro, fecha__day=datetime.now().day,
                                                    fecha__month=datetime.now().month, fecha__year=datetime.now().year)
    capacidad_dia_desarrollador = desarrollador.capacidad_por_dia
    for t in tareas_desarrollador_dia:
        capacidad_dia_desarrollador -= t.horas_trabajadas

    tarea_desarrollador = Tarea.objects.filter(creador=desarrollador.miembro)
    capacidad_desarrollador = desarrollador.capacidad_total
    for t in tarea_desarrollador:
        capacidad_desarrollador -= t.horas_trabajadas

    context = {
        'tablero': tablero,
        'permisos': permisos,
        'proyecto': proyecto,
        'sprint': sprint,
        'us': us,
        'horas_restantes': horas_restantes,
        'horas_trabajadas': us.horas_estimadas - horas_restantes,
        'desarrollador': desarrollador,
        'tareas': tareas,
        'notas': notas,
        'capacidad_dia_desarrollador': capacidad_dia_desarrollador,
        'capacidad_desarrollador': capacidad_desarrollador
    }
    return render(request, 'tableros/tablero_us_detalles.html', context)


@login_required
def actualizar_estado(request, tablero_id, sprint_id, proyecto_id, us_id):
    """
        Clase de la vista para la actualizacion del estado de un US en el tablero
    """
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    tablero = Tablero.objects.get(id=tablero_id)
    us = UserStory.objects.get(id=us_id)
    campos = tablero.campos.split(',')
    indice = campos.index(us.estado)
    estados_siguientes = []

    if indice > 0:
        estados_siguientes.append((campos[indice - 1], campos[indice - 1]))
    if indice < len(campos) - 1:
        estados_siguientes.append((campos[indice + 1], campos[indice + 1]))

    form = ActualizarEstadoForm(instance=us, estados_siguientes=estados_siguientes)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    try:
        desarrollador = Desarrollador.objects.get(miembro__usuario__user=request.user, sprint=sprint)
    except Desarrollador.DoesNotExist:
        desarrollador = []

    if "Visualizar Tablero" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    if request.method == 'POST':
        form = ActualizarEstadoForm(request.POST, instance=us, estados_siguientes=estados_siguientes)
        if form.is_valid():
            form.save()
            return redirect('tableros:tablero_detalles', tablero_id, sprint_id, proyecto_id)

    context = {
        'tablero': tablero,
        'permisos': permisos,
        'proyecto': proyecto,
        'sprint': sprint,
        'us': us,
        'form': form,
        'estados_siguientes': estados_siguientes
    }
    return render(request, 'tableros/actualizar_estado.html', context)


@login_required
def registrar_tarea(request, tablero_id, sprint_id, proyecto_id, us_id):
    """
        Clase de la vista para el registro de tareas dentro de un US en el tablero
    """
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    tablero = Tablero.objects.get(id=tablero_id)
    us = UserStory.objects.get(id=us_id)
    tareas = Tarea.objects.filter(userstory=us)
    mensaje = ""
    form = TareaForm()

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    try:
        desarrollador = Desarrollador.objects.get(miembro__usuario__user=request.user, sprint=sprint)
    except Desarrollador.DoesNotExist:
        return redirect('sprints:acceso_denegado', sprint_id, proyecto_id)

    if "Visualizar Tablero" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    horas_restantes = us.horas_estimadas
    for t in tareas:
        horas_restantes -= t.horas_trabajadas

    tareas_desarrollador_dia = Tarea.objects.filter(creador=desarrollador.miembro, fecha__day=datetime.now().day, fecha__month=datetime.now().month, fecha__year=datetime.now().year)
    capacidad_dia_desarrollador = desarrollador.capacidad_por_dia
    for t in tareas_desarrollador_dia:
        capacidad_dia_desarrollador -= t.horas_trabajadas

    tarea_desarrollador = Tarea.objects.filter(creador=desarrollador.miembro)
    capacidad_desarrollador = desarrollador.capacidad_total
    for t in tarea_desarrollador:
        capacidad_desarrollador -= t.horas_trabajadas

    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            aux = form.save(commit=False)
            if (capacidad_dia_desarrollador - aux.horas_trabajadas) < 0:
                mensaje = "Capacidad del dia excedido"
            elif aux.horas_trabajadas <= 0:
                mensaje = "Las horas trabajadas tienen que ser mayor que 0"
            else:
                aux.userstory = us
                aux.creador = desarrollador.miembro
                aux.fecha = datetime.now()
                aux.save()
                return redirect('tableros:tablero_us_detalles', tablero_id, sprint_id, proyecto_id, us_id)

    context = {
        'tablero': tablero,
        'permisos': permisos,
        'proyecto': proyecto,
        'sprint': sprint,
        'us': us,
        'form': form,
        'mensaje': mensaje,
        'capacidad_dia_desarrollador': capacidad_dia_desarrollador,
        'capacidad_desarrollador': capacidad_desarrollador
    }
    return render(request, 'tableros/registrar_tarea.html', context)


@login_required
def adjuntar_nota(request, tablero_id, sprint_id, proyecto_id, us_id):
    """
        Clase de la vista para el registro de notas dentro de un US en el tablero
    """
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    tablero = Tablero.objects.get(id=tablero_id)
    us = UserStory.objects.get(id=us_id)
    form = NotaForm()

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    try:
        desarrollador = Desarrollador.objects.get(miembro__usuario__user=request.user, sprint=sprint)
    except Desarrollador.DoesNotExist:
        return redirect('sprints:acceso_denegado', sprint_id, proyecto_id)

    if "Visualizar Tablero" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            aux = form.save(commit=False)
            aux.userstory = us
            aux.creador = desarrollador.miembro
            aux.fecha = datetime.now()
            aux.save()
            return redirect('tableros:tablero_us_detalles', tablero_id, sprint_id, proyecto_id, us_id)

    context = {
        'tablero': tablero,
        'permisos': permisos,
        'proyecto': proyecto,
        'sprint': sprint,
        'us': us,
        'desarrollador': desarrollador,
        'form': form
    }
    return render(request, 'tableros/adjuntar_nota.html', context)


@login_required
def aprobar_us(request, tablero_id, sprint_id, proyecto_id, us_id):
    """
        Clase de la vista para la aprobacion de un User Story dentro de un tablero
    """
    us = get_object_or_404(UserStory, pk=us_id)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Aprobar US" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    us.aprobado = True
    us.save()
    return redirect('tableros:tablero_us_detalles', tablero_id, sprint_id, proyecto_id, us_id)
