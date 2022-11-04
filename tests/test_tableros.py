import pytest
from django.urls import reverse

from roles.models import Rol, Permiso
from sprints.models import Sprint
from tipo_us.models import Tipo_US, MiembroTipoUs
from usuarios.models import Usuario
from proyectos.models import Proyecto, Miembro
from tableros.models import Tablero


class TestVistas:

    @pytest.mark.django_db
    def test_listar_tableros(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)
        permisos = []

        client.force_login(user)
        proyecto = Proyecto(nombre='pruebaUnit', descripcion='pruebaUnit')
        proyecto.save()

        permiso = Permiso(nombre="Visualizar Sprints")
        permiso.save()
        permisos.append(permiso)
        permiso = Permiso(nombre="Visualizar Tablero")
        permiso.save()
        permisos.append(permiso)

        rol = Rol.objects.create(nombre="Scrum Master", proyecto=proyecto)
        rol.permiso.add(permisos.pop())
        rol.permiso.add(permisos.pop())
        rol.save()

        miembro = Miembro.objects.create(proyecto=proyecto, usuario=Usuario(user=user))
        miembro.rol.add(rol)
        miembro.save()
        sprint = Sprint.objects.create(proyecto=proyecto)
        sprint.save()

        url = reverse('tableros:index', kwargs={'sprint_id': sprint.id, 'proyecto_id': proyecto.id})
        respuesta = client.get(url)
        assert respuesta.status_code == 200,"Enlace incorrecto"

    @pytest.mark.django_db
    def test_listar_tableros_fail(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)
        permisos = []

        client.force_login(user)
        proyecto = Proyecto(nombre='pruebaUnit', descripcion='pruebaUnit')
        proyecto.save()

        permiso = Permiso(nombre="Visualizar Sprints")
        permiso.save()
        permisos.append(permiso)

        rol = Rol.objects.create(nombre="Scrum Master", proyecto=proyecto)
        rol.save()

        miembro = Miembro.objects.create(proyecto=proyecto, usuario=Usuario(user=user))
        miembro.rol.add(rol)
        miembro.save()
        sprint = Sprint.objects.create(proyecto=proyecto)
        sprint.save()

        url = reverse('tableros:index', kwargs={'sprint_id': sprint.id, 'proyecto_id': proyecto.id})
        respuesta = client.get(url)
        assert respuesta.status_code == 302,"Enlace incorrecto"

class TestModelos:
    @pytest.mark.django_db
    def test_tablero(self, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)
        permisos = []

        proyecto = Proyecto(nombre='pruebaUnit', descripcion='pruebaUnit')
        proyecto.save()

        permiso = Permiso(nombre="Visualizar Sprints")
        permiso.save()
        permisos.append(permiso)
        permiso = Permiso(nombre="Visualizar Tablero")
        permiso.save()
        permisos.append(permiso)

        rol = Rol.objects.create(nombre="Scrum Master", proyecto=proyecto)
        rol.permiso.add(permisos.pop())
        rol.permiso.add(permisos.pop())
        rol.save()

        miembro = Miembro.objects.create(proyecto=proyecto, usuario=Usuario(user=user))
        miembro.rol.add(rol)
        miembro.save()
        sprint = Sprint.objects.create(proyecto=proyecto)
        sprint.save()

        tipo_us = Tipo_US(nombre='prueba_us', descripcion='prueba unitaria')
        tipo_us.save()
        miembro_tipo_us = MiembroTipoUs(proyecto=proyecto, tipo_us=tipo_us)
        miembro_tipo_us.save()

        tablero = Tablero.objects.create(tipo_us=miembro_tipo_us)
        tablero.save()