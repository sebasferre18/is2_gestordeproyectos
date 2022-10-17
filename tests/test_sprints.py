import pytest
from django.urls import reverse

from proyectos.models import Proyecto, Miembro
from roles.models import Rol, Permiso
from sprints.models import Sprint
from tipo_us.models import Tipo_US, MiembroTipoUs
from userstory.models import UserStory
from usuarios.models import Usuario


class TestVistas:

    @pytest.mark.django_db
    def test_listar_sprints(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        proyecto = Proyecto(nombre='pruebaUnit', descripcion='pruebaUnit')
        proyecto.save()
        permiso = Permiso(nombre="Visualizar Sprints")
        permiso.save()
        rol = Rol.objects.create(nombre="Scrum Master", proyecto=proyecto)
        rol.permiso.add(permiso)
        rol.save()
        miembro = Miembro.objects.create(proyecto=proyecto, usuario=Usuario(user=user))
        miembro.rol.add(rol)
        miembro.save()

        url = reverse('sprints:index', kwargs={'proyecto_id': proyecto.id})
        respuesta = client.get(url)
        assert respuesta.status_code == 200

    @pytest.mark.django_db
    def test_listar_sprints_fail(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        proyecto = Proyecto(nombre='pruebaUnit', descripcion='pruebaUnit')
        proyecto.save()

        rol = Rol.objects.create(nombre="Scrum Master", proyecto=proyecto)
        rol.save()

        miembro = Miembro.objects.create(proyecto=proyecto, usuario=Usuario(user=user))
        miembro.rol.add(rol)
        miembro.save()

        url = reverse('sprints:index', kwargs={'proyecto_id': proyecto.id})
        respuesta = client.get(url)
        assert respuesta.status_code == 302


class TestModelos:
    @pytest.mark.django_db
    def test_sprint(self, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)
        sprint = Sprint.objects.create()
        sprint.save()

