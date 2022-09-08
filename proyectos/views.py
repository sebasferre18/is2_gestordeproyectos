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

from proyectos.models import Proyecto
from proyectos.forms import ProyectoForm

def listar_proyectos(request):
    proyecto = Proyecto.objects.all()
    contexto = {'proyectos': proyecto}
    return render(request, 'proyectos/proyectos_list.html', contexto)

def crear_proyecto(request):
    if request.method=='POST':
        formulario = ProyectoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/')
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

def asignar_usuarios(request):
    return render(request, "proyectos/asignar_usuarios.html")

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
def desasignar_usuarios(request):

    #return (request)
    return HttpResponse("Desasignamos usuarios")


def administrar_roles(request):

    #return render(request)
    return HttpResponse("Administramos roles")

'''def eliminar_usuario(request, id_proyecto):
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    proyecto.delete()
    return redirect('usuarios:listar_usuarios')'''