import pytest
from django.urls import reverse
from tipo_us.models import Tipo_US
from usuarios.models import Usuario
from proyectos.models import Proyecto


class TestVistasTipoUs:

    @pytest.mark.django_db
    def test_listar_tipo_us(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        proyecto = Proyecto(nombre='pruebaUnit')
        url = reverse('tipo_us:listar_tipo_us', args={'proyecto_id': proyecto.id})
        respuesta = client.get(url)
        assert respuesta.status_code == 200

    @pytest.mark.django_db
    def test_listar_tipo_us_fail(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        respuesta = client.get('/tipo_us/listar_tipo_us/')
        assert respuesta.status_code == 404

    @pytest.mark.django_db
    def test_crear_tipo_us_fail(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        #proyecto = Proyecto(nombre='pruebaUnit')
        respuesta = client.get('/tipo_us/crear_tipo_us/')
        assert respuesta.status_code == 404

    @pytest.mark.django_db
    def test_modificar_tipo_us(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        tipo_us = Tipo_US(nombre='prueba_us', fecha_creacion='20/04/2022', descripcion='prueba unitaria')
        proyecto = Proyecto(nombre='pruebaUnit')
        url = reverse('tipo_us:modificar_tipo_us', kwargs={'proyecto_id': proyecto.id, 'tipo_us_id': tipo_us.id})
        respuesta = client.get(url)
        assert respuesta.status_code == 200

    def test_modificar_tipo_us_fail(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        respuesta = client.get('/tipo_us/modificar_tipo_us/')
        assert respuesta.status_code == 404

    @pytest.mark.django_db
    def test_eliminar_tipo_us(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        tipo_us = Tipo_US(nombre='prueba_us', fecha_creacion='20/04/2022', descripcion='prueba unitaria')
        proyecto = Proyecto(nombre='pruebaUnit')
        url = reverse('tipo_us:eliminar_tipo_us', kwargs={'proyecto_id': proyecto.id, 'tipo_us_id': tipo_us.id})
        respuesta = client.get(url, follow=True)
        assert respuesta.status_code == 200

    def test_eliminar_tipo_us_fail(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        respuesta = client.get('/tipo_us/eliminar_tipo_us/')
        assert respuesta.status_code == 404


'''
class TestModelos:
    @pytest.mark.django_db
    def test_tipo_us(self):
        tipo_us = Tipo_US(nombre='pruebaus', fecha_creacion='20/04/2022', descripcion="si")

    @pytest.mark.django_db
    def test_tipo_us_comparacion(self):
        tipo_us = Tipo_US(nombre='pruebaus', fecha_creacion='20/04/2022', descripcion="si")
        assert tipo_us.nombre == 'pruebaus'

    @pytest.mark.django_db
    def test_tipo_us_fallo(self):
        tipo_us = Tipo_US(nombre='pruebaus', fecha_creacion='20/04/2022', descripcion="si")
        assert tipo_us.nombre == 123

'''
