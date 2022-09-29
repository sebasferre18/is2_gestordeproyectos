from django.shortcuts import render, get_object_or_404, redirect

from proyectos.models import Proyecto
from usuarios.models import Usuario
from userstory.models import UserStory
from userstory.forms import US_Form
from funciones import obtener_permisos


def listar_us(request, proyecto_id):
    us = UserStory.objects.all().filter(proyecto_id=proyecto_id).order_by('id')

    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    context = {
        'UserStory': us,
        'permisos': permisos,
        'proyecto_id': proyecto_id,
    }

    return render(request, 'userstory/listar_us.html', context)

def crear_us(request, proyecto_id):
    proyecto = Proyecto.objects.get(id=proyecto_id)
    form = US_Form()
    if request.method == 'POST':
        form = US_Form(request.POST)
        if form.is_valid():
            aux = form.save(commit=False)
            aux.proyecto = proyecto
            aux.save()

            return redirect('userstory:listar_us', proyecto_id)

    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    context = {
        'form': form,
        'permisos': permisos,
        'proyecto_id': proyecto_id,
    }
    return render(request, 'userstory/crear_us.html', context)


def modificar_us(request,proyecto_id, us_id):
    us = get_object_or_404(UserStory, pk=us_id)
    form = US_Form(instance=us)

    if request.method == 'POST':
        form = US_Form(request.POST, instance=us)
        if form.is_valid():
            form.save()
            return redirect('userstory:listar_us', proyecto_id)

    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    context = {
        'form': form,
        'permisos': permisos,
        'proyecto_id': proyecto_id,
    }
    return render(request, 'userstory/modificar_us.html', context)
