from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import date

from proyectos.models import Proyecto, Miembro
from proyectos.forms import ProyectoForm, MiembroForm
from usuarios.models import Usuario
from funciones import obtener_permisos

"""
Vistas de la app de Proyectos.
"""

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
        formulario = ProyectoForm(request.POST)
        if formulario.is_valid():
            proyecto = formulario.save()
            miembro.proyecto = proyecto
            miembro.rol = usuario.rol.get(pk=1)
            miembro.save()
            return HttpResponseRedirect('/proyectos/')
    else:
        formulario = ProyectoForm()
    return render(request, 'proyectos/crear_proyecto.html', {'formulario':formulario, 'permisos':permisos})


@login_required
def asignar_usuarios(request, proyecto_id):
    """
    Clase de la vista para la asignacion de miembros en un proyecto
    """
    proyecto = Proyecto.objects.get(id=proyecto_id)
    form = MiembroForm()
    if request.method == 'POST':
        form = MiembroForm(request.POST)
        if form.is_valid():
            miembro = form.save(commit=False)
            miembro.proyecto = proyecto
            miembro.save()
            return redirect('proyectos:ver_detalles', proyecto_id)
    context = {
        'form': form,
        'proyecto_id': proyecto_id,
    }
    return render(request, "proyectos/asignar_usuarios.html", context)

@login_required
def desasignar_usuarios(request, proyecto_id):
    """
    Clase de la vista para la desasignacion de miembros en un proyecto
    """
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    miembros = Miembro.objects.filter(proyecto=proyecto)
    context = {
        'miembros': miembros,
        'proyecto_id': proyecto_id
    }
    return render(request, 'proyectos/desasignar_usuarios.html', context)


@login_required
def eliminar_miembro(request, proyecto_id, miembro_id):
    """
    Clase de la vista para eliminar a un miembro de un proyecto
    """
    miembro = get_object_or_404(Miembro, id=miembro_id)
    miembro.delete()
    return redirect('proyectos:ver_detalles', proyecto_id)


@login_required
def ver_detalles(request, proyecto_id):
    """
    Clase de la vista para la visualizacion de los detalles especificos de un proyecto
    """
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    miembros = Miembro.objects.filter(proyecto=proyecto)

    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    if "Crear Proyecto" not in permisos:
        try:
            miembro = miembros.get(usuario=usuario, proyecto=proyecto)
        except Miembro.DoesNotExist:
            return redirect('proyectos:acceso_denegado')
        rol = miembro.rol
        if rol:
            permisos = obtener_permisos([rol])
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
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    proyecto.estado = 'En ejecucion'
    proyecto.fecha_inicio = date.today()
    proyecto.save()
    return redirect('proyectos:ver_detalles', proyecto_id)


@login_required
def finalizar_proyecto(request, proyecto_id):
    """
    Clase de la vista para la finalizacion de un proyecto
    """
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    proyecto.estado = 'Finalizado'
    proyecto.fecha_fin = date.today()
    proyecto.save()
    return redirect('proyectos:ver_detalles', proyecto_id)


@login_required
def cancelar_proyecto(request, proyecto_id):
    """
    Clase de la vista para la cancelacion de un proyecto
    """
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    proyecto.estado = 'Cancelado'
    proyecto.fecha_fin = date.today()
    proyecto.save()
    return redirect('proyectos:ver_detalles', proyecto_id)

def acceso_denegado(request):
    """
    Clase de la vista de acceso denegado a un proyecto
    """
    return render(request, 'proyectos/acceso_denegado.html')

