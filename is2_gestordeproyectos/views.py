
from django.shortcuts import render
from usuarios.models import Usuario
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from funciones import obtener_permisos


def home(request):
    user = request.user
    permisos = []

    if user.is_authenticated:
        usuario = Usuario.objects.get(user_id=user.id)
        rol = usuario.rol.all()

        permisos = obtener_permisos(rol)

        print(permisos)

    context = {
        'user': user,
        'permisos': permisos,
    }
    return render(request, 'base/home.html', context)
