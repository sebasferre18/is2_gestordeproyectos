from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import date

from tipo_us.models import Tipo_US
from tipo_us.forms import Tipo_usForm
from usuarios.models import Usuario
from funciones import obtener_permisos

# Create your views here.

def listar_tipo_us(request):
    tipo_us = Tipo_US.objects.all().order_by('id')

    form = Tipo_usForm()
    if request.method == 'POST':
        form = Tipo_usForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/tipo_us/')

    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    context = {
        'tipo_us': tipo_us,
        'permisos': permisos
    }

    return render(request, 'tipo_us/listar_tipo_us.html', context)

def crear_tipo_us(request):

    form = Tipo_usForm()
    if request.method == 'POST':
        form = Tipo_usForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/tipo_us/')

    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    context = {
        'form': form,
        'permisos': permisos
    }
    return render(request, 'tipo_us/crear_tipo_us.html', context)


def modificar_tipo_us(request, tipo_us_id):
    tipo_u = get_object_or_404(Tipo_US, pk=tipo_us_id)
    form = Tipo_usForm(instance=tipo_u)

    if request.method == 'POST':
        form = Tipo_usForm(request.POST, instance=tipo_u)
        if form.is_valid():
            form.save()
            return redirect('/tipo_us/')

    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    context = {
        'form': form,
        'permisos': permisos
    }
    return render(request, 'tipo_us/modificar_tipo_us.html', context)


def eliminar_tipo_us(request, tipo_us_id):
    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    tipo_u = get_object_or_404(Tipo_US, pk=tipo_us_id)
    if request.method == 'POST':
        tipo_u.delete()
        return redirect('/tipo_us/')

    context = {
        'tipo_u': tipo_u,
        'permisos': permisos
    }
    return render(request, 'tipo_us/eliminar_tipo_us.html', context)