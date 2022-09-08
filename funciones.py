
def obtener_permisos(rol):
    pe = []
    for r in rol:
        for p in r.permiso.all():
            pe.append(p.nombre)

    return pe
