'''from django.shortcuts import render, HttpResponse'''

# Create your views here.

'''Vistas de la App Proyectos'''

'''def index(request):'''
        #Clase de la vista de la lista de Roles
'''roles = Rol.objects.all().order_by('id')
    context = {
        'role_list': roles
    }'''
    #mensaje = 5

''' return render(request, 'proyectos/index.html')

def crear_proyecto(request):

    return render(request, 'proyectos/proyect_form.html')


def asignar_usuarios(request):

    return render(request)


def desasignar_usuarios(request):

    return render(request)


def administrar_roles(request):

    return render(request)'''

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import date

from proyectos.models import Proyecto, Miembro
from proyectos.forms import ProyectoForm, MiembroForm
from usuarios.models import Usuario
from funciones import obtener_permisos

@login_required
def listar_proyectos(request):
    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    rol = usuario.rol.all()

    permisos = obtener_permisos(rol)

    proyecto = Proyecto.objects.filter(miembro__usuario__user=request.user)

    contexto = {'proyectos': proyecto, 'permisos': permisos}
    return render(request, 'proyectos/proyectos_list.html', contexto)


@login_required
def crear_proyecto(request):
    user = request.user
    usuario = Usuario.objects.get(user_id=user.id)
    miembro = Miembro()
    miembro.usuario = usuario

    if request.method=='POST':
        formulario = ProyectoForm(request.POST)
        if formulario.is_valid():
            proyecto = formulario.save()
            miembro.proyecto = proyecto
            miembro.rol = usuario.rol.get(pk=1)
            miembro.save()
            return HttpResponseRedirect('/proyectos/')
    else:
        formulario = ProyectoForm()
    return render(request,  'proyectos/crear_proyecto.html', {'formulario':formulario})

'''def asignar_usuarios(request, id_proyecto):
    proyecto = get_object_or_404(Proyecto, pk=id_proyecto)
    if request.method == "POST":
        formulario = ProyectoForm(request.POST, instance=proyecto)
        if formulario.is_valid():
            proyecto = formulario.save(commit=False)
            proyecto.save()
            return redirect('proyectos:listar_proyectos')
    else:
        formulario = ProyectoForm(instance=proyecto)
    contexto = {'formulario': formulario}
    return render(request, 'proyectos/modificar_usuario.html', contexto)

def desasignar_usuarios(request, id_proyecto):
    proyecto = get_object_or_404(Proyecto, pk=id_proyecto)
    if request.method == "POST":
        formulario = ProyectoForm(request.POST, instance=proyecto)
        if formulario.is_valid():
            proyecto = formulario.save(commit=False)
            proyecto.save()
            return redirect('proyectos:listar_proyectos')
    else:
        formulario = ProyectoForm(instance=proyecto)
    contexto = {'formulario': formulario}
    return render(request, 'proyectos/modificar_usuario.html', contexto)'''

@login_required
def asignar_usuarios(request, proyecto_id):
    proyecto = Proyecto.objects.get(id=proyecto_id)
    form = MiembroForm()
    if request.method == 'POST':
        form = MiembroForm(request.POST)
        if form.is_valid():
            miembro = form.save(commit=False)
            miembro.proyecto = proyecto
            miembro.save()
            return redirect('proyectos:ver_detalles', proyecto_id)
    context = {
        'form': form,
        'proyecto_id': proyecto_id,
    }
    return render(request, "proyectos/asignar_usuarios.html", context)


@login_required
def asignar_usuarios_busqueda(request):

    '''if request.GET["user"]:

        #mensaje="Articulo buscado: %r" %request.GET["produc"]
        usuario=request.GET["user"]

        if len(usuario)>30:

            mensaje = "Nombre de usuario demasiado largo"

        else:

            articulos=Articulos.objects.filter(nombre__icontains=usuario)

            return render(request, "resultados_busqueda.html", {"articulos":articulos, "query":usuario})
    else:

        mensaje="No has introducido ningun usuario"'''

    return HttpResponse("Funciona")

@login_required
def desasignar_usuarios(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    miembros = Miembro.objects.filter(proyecto=proyecto)
    context = {
        'miembros': miembros,
        'proyecto_id': proyecto_id
    }
    return render(request, 'proyectos/desasignar_usuarios.html', context)


@login_required
def eliminar_miembro(request, proyecto_id, miembro_id):
    miembro = get_object_or_404(Miembro, id=miembro_id)
    miembro.delete()
    return redirect('proyectos:ver_detalles', proyecto_id)


@login_required
def administrar_roles(request):

    #return render(request)
    return HttpResponse("Administramos roles")

'''def eliminar_usuario(request, id_proyecto):
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    proyecto.delete()
    return redirect('usuarios:listar_usuarios')'''

@login_required
def ver_detalles(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    miembros = Miembro.objects.filter(proyecto=proyecto)

    user = request.user

    usuario = Usuario.objects.get(user_id=user.id)
    miembro = miembros.get(usuario=usuario)
    rol = miembro.rol

    if rol:
        permisos = obtener_permisos([rol])
    else:
        permisos = []

    context = {
        'proyecto': proyecto,
        'miembros': miembros,
        'permisos': permisos
    }
    return render(request, 'proyectos/proyecto_detalles.html', context)

@login_required
def iniciar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    proyecto.estado = 'En ejecucion'
    proyecto.fecha_inicio = date.today()
    proyecto.save()
    return redirect('proyectos:ver_detalles', proyecto_id)


@login_required
def finalizar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    proyecto.estado = 'Finalizado'
    proyecto.fecha_fin = date.today()
    proyecto.save()
    return redirect('proyectos:ver_detalles', proyecto_id)


@login_required
def cancelar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    proyecto.estado = 'Cancelado'
    proyecto.fecha_fin = date.today()
    proyecto.save()
    return redirect('proyectos:ver_detalles', proyecto_id)

