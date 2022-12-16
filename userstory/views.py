from django.shortcuts import render, get_object_or_404, redirect
from datetime import date, datetime

from proyectos.models import Proyecto, Miembro, Historial, Notificacion
from usuarios.models import Usuario
from userstory.models import UserStory, Tarea
from userstory.forms import US_Form
from funciones import obtener_permisos


def listar_us(request, proyecto_id):
    """
    Clase de la vista de la lista de User Stories
    """
    us = UserStory.objects.all().filter(proyecto_id=proyecto_id).order_by('id')

    user = request.user
    miembros = Miembro.objects.filter(proyecto_id=proyecto_id)
    usuario = Usuario.objects.get(user_id=user.id)

    miembro_aux = miembros.get(usuario=usuario, proyecto_id=proyecto_id)
    rol = miembro_aux.rol.get_queryset()
    if rol:
        permisos = obtener_permisos(rol)
    else:
        permisos = []

    proyecto = Proyecto.objects.get(id=proyecto_id)

    notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
    cantidad = 0
    for n in notificacion:
        if not n.visto:
            cantidad += 1
    context = {
        'UserStory': us,
        'permisos': permisos,
        'proyecto_id': proyecto_id,
        'proyecto': proyecto,
        'cantidad': cantidad
    }

    return render(request, 'userstory/listar_us.html', context)

def crear_us(request, proyecto_id):
    """
    Clase de la vista para la creacion de User Stories
    """
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    form = US_Form(pro_id=proyecto_id)
    if request.method == 'POST':
        form = US_Form(request.POST, pro_id=proyecto_id)
        if form.is_valid():
            aux = form.save(commit=False)
            aux.proyecto = proyecto
            aux.fecha_creacion = date.today()
            aux.horas_estimadas_original = aux.horas_estimadas
            aux.autor = user.username
            aux.prioridad = (0.6 * aux.business_value + 0.4 * aux.user_point) + aux.sprint_previo
            aux.save()

            informacion = "ID: " + str(aux.id) + "; Nombre: " + aux.nombre + "; Tipo de US: " + \
                          aux.tipo_us.tipo_us.nombre + "; Descripcion: " + aux.descripcion + "; Horas estimadas: " + \
                          str(aux.horas_estimadas) + "; Prioridad tecnica: " + str(aux.user_point) + \
                          "; Prioridad de negocio: " + str(aux.business_value) + "; Prioridad general: " + \
                          str(aux.prioridad)
            historial = Historial(proyecto=proyecto, responsable=usuario, fecha=datetime.now(), accion='Creacion',
                                  elemento='User Stories', informacion=informacion)
            historial.save()
            return redirect('userstory:listar_us', proyecto_id)

    miembros = Miembro.objects.filter(proyecto_id=proyecto_id)

    miembro_aux = miembros.get(usuario=usuario, proyecto_id=proyecto_id)
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
    return render(request, 'userstory/crear_us.html', context)


def modificar_us(request,proyecto_id, us_id):
    """
    Clase de la vista para la modificacion de User Stories
    """
    us = get_object_or_404(UserStory, pk=us_id)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    form = US_Form(instance=us, pro_id=proyecto_id)

    if request.method == 'POST':
        form = US_Form(request.POST, instance=us, pro_id=proyecto_id)
        if form.is_valid():
            aux = form.save(commit=False)
            aux.fecha_modificacion = date.today()
            aux.prioridad = (0.6 * aux.business_value + 0.4 * aux.user_point) + aux.sprint_previo
            aux.save()

            informacion = "ID: " + str(us_id) + "; Nombre: " + aux.nombre + "; Tipo de US: " + \
                          aux.tipo_us.tipo_us.nombre + "; Descripcion: " + aux.descripcion + "; Horas estimadas: " + \
                          str(aux.horas_estimadas) + "; Prioridad tecnica: " + str(aux.user_point) + \
                          "; Prioridad de negocio: " + str(aux.business_value) + "; Prioridad general: " + \
                          str(aux.prioridad)
            historial = Historial(proyecto=proyecto, responsable=usuario, fecha=datetime.now(), accion='Modificacion',
                                  elemento='User Stories', informacion=informacion, userstory=aux)
            historial.save()
            return redirect('userstory:listar_us', proyecto_id)

    miembros = Miembro.objects.filter(proyecto_id=proyecto_id)

    miembro_aux = miembros.get(usuario=usuario, proyecto_id=proyecto_id)
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
    return render(request, 'userstory/modificar_us.html', context)
