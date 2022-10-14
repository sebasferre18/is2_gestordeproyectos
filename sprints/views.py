from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from funciones import obtener_permisos, obtener_permisos_usuario

# Create your views here.
from proyectos.models import Proyecto, Miembro
from .forms import SprintForm
from .models import Sprint


@login_required
def index(request, proyecto_id):
    """
    Clase de la vista de la lista de User Stories
    """
    sprints = Sprint.objects.all().filter(proyecto_id=proyecto_id).order_by('id')

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Visualizar Sprints" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    proyecto = Proyecto.objects.get(id=proyecto_id)
    context = {
        'sprints': sprints,
        'permisos': permisos,
        'proyecto': proyecto,
    }

    return render(request, 'sprints/listar_sprints.html', context)


@login_required
def ver_detalles(request, sprint_id, proyecto_id):
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

    context = {
        'form': form,
        'permisos': permisos,
        'proyecto': proyecto
    }
    return render(request, 'sprints/crear_sprint.html', context)

