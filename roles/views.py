from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Rol
from .forms import RolForm

# Create your views here.


def index(request):
    roles = Rol.objects.all().order_by('id')
    context = {
        'role_list': roles
    }
    return render(request, 'roles/index.html', context)


def crear_rol(request):
    form = RolForm()
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/roles/')

    context = {
        'form': form
    }
    return render(request, 'roles/rol_form.html', context)


def modificar_rol(request, rol_id):
    rol = get_object_or_404(Rol, pk=rol_id)
    form = RolForm(instance=rol)

    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            form.save()
            return redirect('/roles/')

    context = {
        'form': form
    }
    return render(request, 'roles/rol_form.html', context)


def eliminar_rol(request, rol_id):
    rol = get_object_or_404(Rol, pk=rol_id)
    if request.method == 'POST':
        rol.delete()
        return redirect('/roles/')

    context = {
        'rol': rol
    }
    return render(request, 'roles/eliminar_rol.html', context)

