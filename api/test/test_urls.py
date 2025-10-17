from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase
from api.views.usuario_view_set import UsuarioViewSet
from api.views.producto_view_set import ProductoViewSet
from api.views.register_view_set import RegisterViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class URLPatternsTest(APITestCase):
    def test_usuario_list_url_resolves(self):
        url = reverse('usuario-list')
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, UsuarioViewSet)

    def test_usuario_detail_url_resolves(self):
        url = reverse('usuario-detail', args=[1])
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, UsuarioViewSet)

    def test_producto_list_url_resolves(self):
        url = reverse('producto-list')
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, ProductoViewSet)

    def test_producto_detail_url_resolves(self):
        url = reverse('producto-detail', args=[1])
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, ProductoViewSet)

    def test_register_url_resolves(self):
        url = reverse('register')
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, RegisterViewSet)

    def test_token_obtain_url_resolves(self):
        url = reverse('token_obtain_pair')
        resolver = resolve(url)
        # SimpleJWT usa as_view, la vista será TokenObtainPairView
        self.assertEqual(resolver.func.view_class, TokenObtainPairView)

    def test_token_refresh_url_resolves(self):
        url = reverse('token_refresh')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, TokenRefreshView)

    def test_rutas_existentes_devuelven_200_o_401(self):
        # /users/ requiere autenticación, debe devolver 401
        url = reverse('usuario-list')
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_200_OK])

        url = reverse('producto-list')
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_200_OK])

        url = reverse('register')
        response = self.client.post(url, {})  # POST, pero vacío
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_201_CREATED])

        url = reverse('token_obtain_pair')
        response = self.client.post(url, {})  # POST, pero vacío
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_200_OK])

        url = reverse('token_refresh')
        response = self.client.post(url, {})  # POST, pero vacío
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_200_OK])