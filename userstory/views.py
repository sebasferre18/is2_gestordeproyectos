from django.shortcuts import render, get_object_or_404, redirect
from usuarios.models import Usuario
from userstory.models import UserStory
from userstory.forms import US_Form
from funciones import obtener_permisos


def listar_us(request):
    us = UserStory.objects.all().order_by('id')

    form = US_Form()
    if request.method == 'POST':
        form = US_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/listar_us/')

    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    context = {
        'us': us,
        'permisos': permisos
    }

    return render(request, 'userstory/listar_us.html', context)

def crear_us(request):

    form = US_Form()
    if request.method == 'POST':
        form = US_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/crear_us/')

    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    context = {
        'form': form,
        'permisos': permisos
    }
    return render(request, 'userstory/crear_us.html', context)


def modificar_us(request, tipo_us_id):
    us = get_object_or_404(UserStory, pk=tipo_us_id)
    form = US_Form(instance=us)

    if request.method == 'POST':
        form = US_Form(request.POST, instance=us)
        if form.is_valid():
            form.save()
            return redirect('/listar_us/')

    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    context = {
        'form': form,
        'permisos': permisos
    }
    return render(request, 'userstory/modificar_us.html', context)
