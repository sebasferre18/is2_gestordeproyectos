from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import date

from tipo_us.models import Tipo_US, MiembroTipoUs
from tipo_us.forms import Tipo_usForm
from proyectos.models import Proyecto, Miembro
from usuarios.models import Usuario
from funciones import obtener_permisos

# Create your views here.

def listar_tipo_us(request, proyecto_id):
    """
    Clase de la vista de la lista de tipos de User Stories
    """
    #tipo_us = Tipo_US.objects.all().order_by('id')
    #proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    miembro_tipo_us = MiembroTipoUs.objects.filter(proyecto=proyecto)

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

def crear_tipo_us(request, proyecto_id):
    """
    Clase de la vista para la creacion de tipos de User Stories
    """
    #proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    miembro = MiembroTipoUs()
    miembro.proyecto = proyecto

    form = Tipo_usForm()
    if request.method == 'POST':
        form = Tipo_usForm(request.POST)
        if form.is_valid():
            tipo_us = form.save()
            #tipo_us.fecha_creacion = date.today()
            miembro.tipo_us = tipo_us
            miembro.save()
            return HttpResponseRedirect('/tipo_us/' + str(proyecto_id) + '/')


    context = {
        'form': form,
        'proyecto': proyecto
    }
    return render(request, 'tipo_us/crear_tipo_us.html', context)

def modificar_tipo_us(request, proyecto_id, tipo_us_id):
    """
    Clase de la vista para la creacion de tipos de User Stories
    """
    proyecto = Proyecto.objects.get(id=proyecto_id)
    miembro_tipo_us = get_object_or_404(MiembroTipoUs, id=tipo_us_id)
    tipo_us = miembro_tipo_us.tipo_us
    form = Tipo_usForm(instance=tipo_us)

    if request.method == 'POST':
        form = Tipo_usForm(request.POST, instance=tipo_us)
        if form.is_valid():
            form.save()
            return redirect('/tipo_us/' + str(proyecto_id) + '/')

    context = {
        'form': form,
        'proyecto': proyecto
    }
    return render(request, 'tipo_us/modificar_tipo_us.html', context)


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

def agregar_tipo_us(request, proyecto_id, tipo_us_id):
    """
    Clase de la vista para agregar un tipo de US a un proyecto
    """
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    tipo_us = get_object_or_404(Tipo_US, id=tipo_us_id)

    tipo_us_aux = Tipo_US(nombre=tipo_us.nombre, fecha_creacion=tipo_us.fecha_creacion, descripcion=tipo_us.descripcion)
    tipo_us_aux.save()

    miembro = MiembroTipoUs(proyecto=proyecto, tipo_us=tipo_us_aux)
    miembro.save()
    return redirect('tipo_us:importar_tipo_us', proyecto_id)