import pytest
from usuarios.models import Usuario
from django.test import Client


class TestVistas:

    def test_listar_usuario(self, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)
        client = Client()
        client.force_login(user)
        respuesta = client.get('/usuarios/listar_usuarios/')
        assert respuesta.status_code == 200

    def test_nuevo_usuario(self, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)
        client = Client()
        client.force_login(user)
        respuesta = client.get('/usuarios/nuevo_usuario/')
        assert respuesta.status_code == 200

    @pytest.mark.django_db
    def test_modificar_usuario(self, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)
        usuario = Usuario(user=user)
        client = Client()
        client.force_login(user)
        respuesta = client.get('/1/modificar_usuario/')
        assert respuesta.status_code == 200


class TestModelos:

    def test_usuario(self, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)
        usuario = Usuario(user=user, ci=1234567, telefono="0444 444444", fecha_nac="01/01/1998")

