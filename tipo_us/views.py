from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import date

from tableros.models import Tablero
from tipo_us.models import Tipo_US, MiembroTipoUs
from tipo_us.forms import Tipo_usForm
from proyectos.models import Proyecto, Miembro
from usuarios.models import Usuario
from funciones import obtener_permisos, obtener_permisos_usuario


# Create your views here.
@login_required
def listar_tipo_us(request, proyecto_id):
    """
    Clase de la vista de la lista de tipos de User Stories
    """
    #tipo_us = Tipo_US.objects.all().order_by('id')
    #proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    miembro_tipo_us = MiembroTipoUs.objects.filter(proyecto=proyecto).order_by('id')

    user = request.user
    miembros = Miembro.objects.filter(proyecto_id=proyecto_id)
    usuario = Usuario.objects.get(user_id=user.id)

    miembro_aux = miembros.get(usuario=usuario, proyecto_id=proyecto_id)
    rol = miembro_aux.rol.get_queryset()
    if rol:
        permisos = obtener_permisos(rol)
    else:
        permisos = []

    #Aun no se tiene seguridad si es necesario implementar este condicional
    '''if "Crear Tipo US" not in permisos:
        miembro = miembro_tipo_us.get(usuario=usuario)
        rol = miembro.rol
        if rol:
            permisos = obtener_permisos([rol])
        else:
            permisos = []'''

    context = {
        #'tipo_us': tipo_us,
        'permisos': permisos,
        'proyecto': proyecto,
        'miembro_tipo_us': miembro_tipo_us,
    }

    '''form = Tipo_usForm()
    if request.method == 'POST':
        form = Tipo_usForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/tipo_us/')'''

    return render(request, 'tipo_us/listar_tipo_us.html', context)


@login_required
def crear_tipo_us(request, proyecto_id):
    """
    Clase de la vista para la creacion de tipos de User Stories
    """
    #proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    miembro = MiembroTipoUs()
    tablero = Tablero()
    miembro.proyecto = proyecto

    form = Tipo_usForm()
    if request.method == 'POST':
        form = Tipo_usForm(request.POST)
        if form.is_valid():
            tipo_us = form.save()
            #tipo_us.fecha_creacion = date.today()
            miembro.tipo_us = tipo_us
            miembro.save()
            tablero.tipo_us = miembro
            if miembro.tipo_us.campos:
                tablero.campos += "," + miembro.tipo_us.campos
            tablero.save()
            return HttpResponseRedirect('/tipo_us/' + str(proyecto_id) + '/')


    context = {
        'form': form,
        'proyecto': proyecto
    }
    return render(request, 'tipo_us/crear_tipo_us.html', context)


@login_required
def modificar_tipo_us(request, proyecto_id, tipo_us_id):
    """
    Clase de la vista para la creacion de tipos de User Stories
    """
    proyecto = Proyecto.objects.get(id=proyecto_id)
    miembro_tipo_us = get_object_or_404(MiembroTipoUs, id=tipo_us_id)
    tipo_us = miembro_tipo_us.tipo_us
    tablero = Tablero.objects.get(tipo_us=miembro_tipo_us)
    form = Tipo_usForm(instance=tipo_us)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Modificar Tipo US" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    if request.method == 'POST':
        form = Tipo_usForm(request.POST, instance=tipo_us)
        if form.is_valid():
            aux = form.save(commit=False)
            tablero.campos = "Pendiente,En curso,Terminado"
            if aux.campos:
                tablero.campos += "," + aux.campos
            aux.save()
            tablero.save()
            return redirect('/tipo_us/' + str(proyecto_id) + '/')

    context = {
        'form': form,
        'proyecto': proyecto
    }
    return render(request, 'tipo_us/modificar_tipo_us.html', context)


@login_required
def eliminar_tipo_us(request, proyecto_id, tipo_us_id):
    """
    Clase de la vista para la creacion de tipos de User Stories
    """
    proyecto = Proyecto.objects.get(id=proyecto_id)
    miembro_tipo_us = get_object_or_404(MiembroTipoUs, id=tipo_us_id)
    tipo_us = get_object_or_404(Tipo_US, id=miembro_tipo_us.tipo_us.id)

    if request.method == 'POST':
        miembro_tipo_us.delete()
        tipo_us.delete()
        return redirect('/tipo_us/' + str(proyecto_id) + '/')

    context = {
        'miembro_tipo_us': miembro_tipo_us,
        'proyecto': proyecto
    }
    return render(request, 'tipo_us/eliminar_tipo_us.html', context)


@login_required
def importar_tipo_us(request, proyecto_id):
    """
    Clase de la vista para la importacion de Tipo de US en un proyecto
    """
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    miembros_tipo_us = MiembroTipoUs.objects.filter(proyecto=proyecto)
    ids = []

    for a in miembros_tipo_us:
        ids.append(a.tipo_us.id)

    tipos_us = Tipo_US.objects.exclude(id__in=ids)
    miembros_tipo_us = MiembroTipoUs.objects.exclude(tipo_us_id__in=ids).order_by('proyecto')

    user = request.user
    miembros = Miembro.objects.filter(proyecto_id=proyecto_id)
    usuario = Usuario.objects.get(user_id=user.id)

    miembro_aux = miembros.get(usuario=usuario, proyecto_id=proyecto_id)
    rol = miembro_aux.rol.get_queryset()
    if rol:
        permisos = obtener_permisos(rol)
    else:
        permisos = []

    context = {
        'tipos_us': tipos_us,
        'miembros_tipos_us': miembros_tipo_us,
        'permisos': permisos,
        'proyecto_id': proyecto_id,
        'proyecto': proyecto,
    }
    return render(request, "tipo_us/importar_tipo_us.html", context)

@login_required
def agregar_tipo_us(request, proyecto_id, tipo_us_id):
    """
    Clase de la vista para agregar un tipo de US a un proyecto
    """
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    tipo_us = get_object_or_404(Tipo_US, id=tipo_us_id)
    tablero = Tablero()
    tablero_aux = Tablero.objects.get(tipo_us__tipo_us=tipo_us)

    tipo_us_aux = Tipo_US(nombre=tipo_us.nombre, fecha_creacion=tipo_us.fecha_creacion, descripcion=tipo_us.descripcion, campos=tipo_us.campos)
    tipo_us_aux.save()

    miembro = MiembroTipoUs(proyecto=proyecto, tipo_us=tipo_us_aux)
    miembro.save()

    tablero.tipo_us = miembro
    if miembro.tipo_us.campos:
        tablero.campos = tablero_aux.campos
    tablero.save()
    return redirect('tipo_us:importar_tipo_us', proyecto_id)

@login_required
def ordenar_campos(request, proyecto_id, tipo_us_id):
    """
    Clase de la vista para agregar un tipo de US a un proyecto
    """
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    miembro_tipo_us = get_object_or_404(MiembroTipoUs, pk=tipo_us_id)
    tablero = Tablero.objects.get(tipo_us=miembro_tipo_us)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Modificar Tipo US" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    context = {
        'tipo_us': miembro_tipo_us,
        'permisos': permisos,
        'proyecto_id': proyecto_id,
        'proyecto': proyecto,
        'campos': tablero.campos.split(','),
        'len': len(tablero.campos.split(','))
    }
    return render(request, "tipo_us/ordenar_campos_tipo_us.html", context)

@login_required
def ascender(request, proyecto_id, tipo_us_id, campo_id):
    """
    Clase de la vista para cambiar el orden de los campos de forma ascendiente dentro de un tipo de US
    """
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    miembro_tipo_us = get_object_or_404(MiembroTipoUs, pk=tipo_us_id)
    tablero = Tablero.objects.get(tipo_us=miembro_tipo_us)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Modificar Tipo US" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    campos = tablero.campos.split(",")
    campos[campo_id], campos[campo_id - 1] = campos[campo_id - 1], campos[campo_id]

    tablero.campos = ""
    for i, c in enumerate(campos):
        tablero.campos += c
        if i < len(campos) - 1:
            tablero.campos += ","
    tablero.save()

    return redirect('tipo_us:ordenar_campos', proyecto_id, tipo_us_id)


@login_required
def descender(request, proyecto_id, tipo_us_id, campo_id):
    """
    Clase de la vista para agregar un tipo de US a un proyecto
    """
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    miembro_tipo_us = get_object_or_404(MiembroTipoUs, pk=tipo_us_id)
    tablero = Tablero.objects.get(tipo_us=miembro_tipo_us)

    try:
        permisos = obtener_permisos_usuario(request.user, proyecto_id)
    except Miembro.DoesNotExist:
        return redirect('proyectos:acceso_denegado')

    if "Modificar Tipo US" not in permisos:
        return redirect('proyectos:falta_de_permisos', proyecto_id)

    campos = tablero.campos.split(",")
    campos[campo_id], campos[campo_id + 1] = campos[campo_id + 1], campos[campo_id]

    tablero.campos = ""
    for i, c in enumerate(campos):
        tablero.campos += c
        if i < len(campos) - 1:
            tablero.campos += ","
    tablero.save()

    return redirect('tipo_us:ordenar_campos', proyecto_id, tipo_us_id)


