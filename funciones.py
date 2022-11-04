from django.shortcuts import redirect

from proyectos.models import Miembro
from usuarios.models import Usuario


def obtener_permisos(rol):
    """Funcion de obtener los permisos de un rol
        Retorna todos los permisos de un rol en especifico"""
    pe = []
    for r in rol:
        for p in r.permiso.all():
            pe.append(p.nombre)

    return pe


def obtener_permisos_usuario(user, proyecto_id):
    """Funcion de obtener los permisos de un usuario
        Retorna todos los permisos que tiene un usuario en especifico"""
    miembros = Miembro.objects.filter(proyecto_id=proyecto_id)
    usuario = Usuario.objects.get(user_id=user.id)

    miembro_aux = miembros.get(usuario=usuario, proyecto_id=proyecto_id)
    rol = miembro_aux.rol.get_queryset()
    if rol:
        permisos = obtener_permisos(rol)
    else:
        permisos = []

    return permisos


