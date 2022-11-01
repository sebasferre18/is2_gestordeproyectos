from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from funciones import obtener_permisos_usuario
from proyectos.models import Proyecto, Miembro
from sprints.models import Sprint
from tipo_us.models import MiembroTipoUs
from userstory.models import UserStory
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

    campos = tablero.campos

    context = {
        'tablero': tablero,
        'permisos': permisos,
        'proyecto': proyecto,
        'sprint': sprint,
        'campos': campos.split(','),
        'us': us
    }
    return render(request, 'tableros/tablero_detalles.html', context)
