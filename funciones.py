
def obtener_permisos(rol):
    """Funcion de obtener los permisos de un rol

        Retorna todos los permisos de un rol en especifico"""
    pe = []
    for r in rol:
        for p in r.permiso.all():
            pe.append(p.nombre)

    return pe
