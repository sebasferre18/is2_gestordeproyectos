from django.shortcuts import render

from proyectos.models import Notificacion
from usuarios.models import Usuario
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from funciones import obtener_permisos


def home(request):
    user = request.user
    permisos = []

    cantidad = 0
    if user.is_authenticated:
        usuario = Usuario.objects.get(user_id=user.id)
        rol = usuario.rol.all()

        permisos = obtener_permisos(rol)

        notificacion = Notificacion.objects.filter(destinatario=usuario).order_by('-id')
        for n in notificacion:
            if not n.visto:
                cantidad += 1

        print(permisos)

    context = {
        'user': user,
        'permisos': permisos,
        'cantidad': cantidad,
    }
    return render(request, 'base/home.html', context)
