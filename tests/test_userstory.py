import pytest
from django.urls import reverse

from proyectos.models import Proyecto, Miembro
from tipo_us.models import Tipo_US, MiembroTipoUs
from userstory.models import UserStory
from usuarios.models import Usuario


class TestVistas:

    @pytest.mark.django_db
    def test_listar_us(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        proyecto = Proyecto(nombre='pruebaUnit', descripcion='pruebaUnit')
        proyecto.save()
        miembro = Miembro(proyecto=proyecto, usuario=Usuario(user=user))
        miembro.save()

        url = reverse('userstory:listar_us', kwargs={'proyecto_id': proyecto.id})
        respuesta = client.get(url)
        assert respuesta.status_code == 200 ,"Página no encontrada"

    @pytest.mark.django_db
    def test_crear_us(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        proyecto = Proyecto(nombre='pruebaUnit', descripcion='pruebaUnit')
        proyecto.save()
        miembro = Miembro(proyecto=proyecto, usuario=Usuario(user=user))
        miembro.save()

        url = reverse('userstory:crear_us', kwargs={'proyecto_id': proyecto.id})
        respuesta = client.get(url)
        assert respuesta.status_code == 200,"Página no encontrada"

    @pytest.mark.django_db
    def test_modificar_us(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        proyecto = Proyecto(nombre='pruebaUnit', descripcion='pruebaUnit')
        proyecto.save()
        miembro = Miembro(proyecto=proyecto, usuario=Usuario(user=user))
        miembro.save()
        tipo_us = Tipo_US(nombre='prueba_us', descripcion='prueba unitaria')
        tipo_us.save()
        miembro_tipo_us = MiembroTipoUs(proyecto=proyecto, tipo_us=tipo_us)
        miembro_tipo_us.save()
        us = UserStory(nombre="US 1", tipo_us=miembro_tipo_us, descripcion="E")
        us.save()

        url = reverse('userstory:modificar_us', kwargs={'proyecto_id': proyecto.id, 'us_id': us.id})
        respuesta = client.get(url, follow=True)
        assert respuesta.status_code == 200,"Página no encontrada"


class TestModelos:

    @pytest.mark.django_db
    def test_userstory(self, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        proyecto = Proyecto(nombre='pruebaUnit', descripcion='pruebaUnit')
        proyecto.save()
        miembro = Miembro(proyecto=proyecto, usuario=Usuario(user=user))
        miembro.save()
        tipo_us = Tipo_US(nombre='prueba_us', descripcion='prueba unitaria')
        tipo_us.save()
        miembro_tipo_us = MiembroTipoUs(proyecto=proyecto, tipo_us=tipo_us)
        miembro_tipo_us.save()
        us = UserStory(nombre="US 1", tipo_us=miembro_tipo_us, descripcion="E")
        us.save()

