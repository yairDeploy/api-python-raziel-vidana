from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from api.models.usuario import Usuario

User = get_user_model()

class UsuarioViewSetTest(APITestCase):
    def setUp(self):
        # Crear usuario admin y obtener JWT
        self.admin = User.objects.create_user(
            username='adminuser',
            password='adminpass123',
            email='admin@test.com',
            is_staff=True,
            is_superuser=True
        )
        refresh = RefreshToken.for_user(self.admin)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Crear un usuario de ejemplo
        self.usuario = Usuario.objects.create_user(
            username='zpeda',
            password='superseguro',
            email='zpeda@ejemplo.com',
            first_name='Zulema',
            last_name='Pérez',
            edad=28,
            activo=True
        )
        self.list_url = reverse('usuario-list')  # Ajusta según tu router de DRF

    def test_listar_usuarios(self):
        response = self.client.get(self.list_url)
        # Para no depender del orden de los usuarios en la respuesta
        usernames = [u['username'] for u in response.data]
        self.assertIn('zpeda', usernames)
        self.assertIn('adminuser', usernames)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recuperar_usuario(self):
        url = reverse('usuario-detail', args=[self.usuario.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'zpeda')

    def test_eliminar_usuario(self):
        url = reverse('usuario-detail', args=[self.usuario.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Usuario.objects.filter(id=self.usuario.id).exists())

    def test_permiso_no_autenticado(self):
        self.client.credentials()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crear_usuario(self):
        data = {
            'username': 'juanito',
            'nombre': 'Juan',
            'apellido': 'Gómez',
            'edad': 22,
            'activo': True
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Usuario.objects.count(), 3)  # Considerando que ya creaste adminuser y zpeda en setUp
        usuario = Usuario.objects.last()
        self.assertEqual(usuario.username, 'juanito')
        self.assertEqual(usuario.first_name, 'Juan')
        self.assertEqual(usuario.last_name, 'Gómez')
        self.assertEqual(usuario.edad, 22)
        self.assertTrue(usuario.is_active)

    def test_actualizar_usuario(self):
        url = reverse('usuario-detail', args=[self.usuario.id])
        data = {
            'username': 'zpeda',
            'nombre': 'Zulema Actualizada',
            'apellido': 'Pérez Mod',
            'edad': 31,
            'activo': False
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.first_name, 'Zulema Actualizada')
        self.assertEqual(self.usuario.last_name, 'Pérez Mod')
        self.assertEqual(self.usuario.edad, 31)
        self.assertFalse(self.usuario.is_active)

    