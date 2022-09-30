import pytest
from django.urls import reverse

from usuarios.models import Usuario

'''
class TestVistas:
    @pytest.mark.django_db
    def test_listar_usuario(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        url = reverse('usuarios:listar_usuarios')
        respuesta = client.get(url)
        assert respuesta.status_code == 200

    @pytest.mark.django_db
    def test_listar_usuario_fail(self, client, django_user_model):
        respuesta = client.get('/usuarios/listar_usuarios/')
        assert respuesta.status_code == 302

    @pytest.mark.django_db
    def test_nuevo_usuario(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        respuesta = client.get('/usuarios/nuevo_usuario/')
        assert respuesta.status_code == 200

    @pytest.mark.django_db
    def test_modificar_usuario(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        usuario = Usuario(user=user)
        url = reverse('usuarios:modificar_usuario', kwargs={'id_usuario': usuario.user_id})
        respuesta = client.get(url)
        assert respuesta.status_code == 200

    @pytest.mark.django_db
    def test_eliminar_usuario(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)
        dummy = django_user_model.objects.create_user(username="test", password="test")

        client.force_login(user)
        usuario = Usuario(user=dummy)
        url = reverse('usuarios:eliminar_usuario', kwargs={'id_usuario': usuario.user_id})
        respuesta = client.get(url, follow=True)
        assert respuesta.status_code == 200


class TestModelos:
    @pytest.mark.django_db
    def test_usuario(self, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)
        usuario = Usuario(user=user, ci=1234567, telefono="0444 444444", fecha_nac="01/01/1998")
        
'''