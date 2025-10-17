from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from api.models.producto import Producto

User = get_user_model()

class ProductoViewSetTest(APITestCase):
    def setUp(self):
        # Crear usuario y obtener JWT
        self.user = User.objects.create_user(username='testuser', password='pass12345')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Crear un producto de ejemplo
        self.producto = Producto.objects.create(
            nombre='Camiseta',
            precio=99.99,
            stock=10,
            activo=True
        )
        # Ajusta el nombre del endpoint según tu router DRF
        self.list_url = reverse('producto-list')

    def test_listar_productos(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.data[0]['nombre'], 'Camiseta')

    def test_crear_producto(self):
        data = {
            'nombre': 'Pantalón',
            'precio': 150.50,
            'stock': 5,
            'activo': True
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Producto.objects.count(), 2)
        self.assertEqual(Producto.objects.last().nombre, 'Pantalón')

    def test_recuperar_producto(self):
        url = reverse('producto-detail', args=[self.producto.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Camiseta')

    def test_actualizar_producto(self):
        url = reverse('producto-detail', args=[self.producto.id])
        data = {
            'nombre': 'Camiseta Actualizada',
            'precio': 120.00,
            'stock': 8,
            'activo': True
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Camiseta Actualizada')

    def test_eliminar_producto(self):
        url = reverse('producto-detail', args=[self.producto.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Producto.objects.filter(id=self.producto.id).exists())

    def test_permiso_no_autenticado(self):
        self.client.credentials()  # Limpiar credenciales (logout)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)