from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import date

from tipo_us.models import Tipo_US, MiembroTipoUs
from tipo_us.forms import Tipo_usForm
from proyectos.models import Proyecto
from usuarios.models import Usuario
from funciones import obtener_permisos

# Create your views here.

def listar_tipo_us(request, proyecto_id):
    #tipo_us = Tipo_US.objects.all().order_by('id')
    #proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    proyecto = Proyecto.objects.get(id=proyecto_id)
    miembro_tipo_us = MiembroTipoUs.objects.filter(proyecto=proyecto)

    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()
    permisos = obtener_permisos(rol)

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
    proyecto = Proyecto.objects.get(id=proyecto_id)
    miembro_tipo_us = get_object_or_404(MiembroTipoUs, id=tipo_us_id)

    if request.method == 'POST':
        miembro_tipo_us.delete()
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

    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()
    permisos = obtener_permisos(rol)

    context = {
        'tipos_us': tipos_us,
        'permisos': permisos,
        'proyecto_id': proyecto_id
    }
    return render(request, "tipo_us/importar_tipo_us.html", context)

def agregar_tipo_us(request, proyecto_id, tipo_us_id):
    """
    Clase de la vista para eliminar a un miembro de un proyecto
    """
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    tipo_us = get_object_or_404(Tipo_US, id=tipo_us_id)

    miembro = MiembroTipoUs(proyecto=proyecto, tipo_us=tipo_us)
    miembro.save()
    return redirect('tipo_us:importar_tipo_us', proyecto_id)