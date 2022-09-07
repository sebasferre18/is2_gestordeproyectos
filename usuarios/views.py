from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from usuarios.models import Usuario
from usuarios.forms import UsuarioForm

def nuevo_usuario(request):
    if request.method=='POST':
        formulario = UsuarioForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        formulario = UsuarioForm()
    return render(request,  'usuarios/nuevousuario.html', {'formulario':formulario})

def modificar_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, pk=id_usuario)
    if request.method == "POST":
        formulario = UsuarioForm(request.POST, instance=usuario)
        if formulario.is_valid():
            usuario = formulario.save(commit=False)
            usuario.save()
            return redirect('usuarios:listar_usuarios')
    else:
        formulario = UsuarioForm(instance=usuario)
    contexto = {'formulario': formulario}
    return render(request, 'usuarios/modificar_usuario.html', contexto)


def usuario_list(request):
    usuario = Usuario.objects.all()
    contexto = {'usuarios': usuario}
    return render(request, 'usuarios/usuarios_list.html', contexto)
