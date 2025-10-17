from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterViewSetTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')

    def test_registro_usuario_exitoso(self):
        data = {
            'username': 'nuevo_usuario',
            'email': 'nuevo@correo.com',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'edad': 21,
            'password': 'claveSegura123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='nuevo_usuario').exists())
        usuario = User.objects.get(username='nuevo_usuario')
        self.assertTrue(usuario.check_password('claveSegura123'))
        self.assertEqual(usuario.edad, 21)

    def test_registro_usuario_password_corta(self):
        data = {
            'username': 'usuario_corto',
            'email': 'corto@correo.com',
            'first_name': 'Corto',
            'last_name': 'Pass',
            'edad': 18,
            'password': '123'  # Muy corta
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_registro_usuario_faltan_campos(self):
        data = {
            'username': 'incompleto'
            # Falta email, password, etc.
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)