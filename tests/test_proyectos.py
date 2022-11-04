import pytest
from django.urls import reverse

from proyectos.models import Proyecto, Miembro
from tipo_us.models import Tipo_US, MiembroTipoUs
from userstory.models import UserStory
from usuarios.models import Usuario


class TestVistas:

    @pytest.mark.django_db
    def test_listar_proyectos(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        url = reverse('proyectos:listar_proyectos')
        respuesta = client.get(url)
        assert respuesta.status_code == 200

    @pytest.mark.django_db
    def test_proyecto_detalles(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        proyecto = Proyecto.objects.create(nombre='pruebaUnit', descripcion='pruebaUnit')
        proyecto.save()
        miembro = Miembro(proyecto=proyecto, usuario=Usuario(user=user))
        miembro.save()

        url = reverse('proyectos:ver_detalles', kwargs={'proyecto_id': proyecto.id})
        respuesta = client.get(url)
        assert respuesta.status_code == 200

class TestModelos:
    @pytest.mark.django_db
    def test_proyecto(self, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)
        proyecto = Proyecto(nombre='pruebaUnit', descripcion='pruebaUnit')
        proyecto.save()