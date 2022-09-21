from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.forms.formsets import formset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from usuarios.models import Usuario, User
from usuarios.forms import UsuarioForm, UserForm, UsuarioFormSet

@login_required
def nuevo_usuario(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        usuario_form = UsuarioFormSet(request.POST)
        if user_form.is_valid() and usuario_form.is_valid():
            user = user_form.save()

            for a in usuario_form.forms:
                up = a.save(commit=False)
                up.user = user
                up.save()

            return HttpResponseRedirect('/usuarios/listar_usuarios/')
    else:
        user_form = UserForm()
        usuario_form = UsuarioFormSet()
    return render(request,  'usuarios/nuevousuario.html', {'usuario': user_form, 'formulario':usuario_form})

@login_required
def modificar_usuario(request, id_usuario):
    user = get_object_or_404(User, pk=id_usuario)
    usuario = get_object_or_404(Usuario, pk=id_usuario)
    user_form = UserForm(instance=user)
    usuario_form = UsuarioFormSet(instance=usuario)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        usuario_form = UsuarioFormSet(request.POST, instance=usuario)
        if user_form.is_valid() and usuario_form.is_valid():
            user = user_form.save()

            for a in usuario_form.forms:
                up = a.save(commit=False)
                up.user = user
                up.save()

            return HttpResponseRedirect('/usuarios/listar_usuarios/')

    contexto = {'usuario': user_form, 'formulario':usuario_form}
    return render(request, 'usuarios/modificar_usuario.html', contexto)

@login_required
def usuario_list(request):
    usuario = Usuario.objects.all().order_by('user')
    contexto = {'usuarios': usuario}
    return render(request, 'usuarios/usuarios_list.html', contexto)

@login_required
def eliminar_usuario(request, id_usuario):
    user = get_object_or_404(User, id=id_usuario)
    user.delete()
    return redirect('usuarios:listar_usuarios')
