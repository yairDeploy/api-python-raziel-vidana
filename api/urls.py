from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views.producto_view_set import ProductoViewSet
from api.views.register_view_set import RegisterViewSet
from api.views.usuario_view_set import UsuarioViewSet

router = DefaultRouter()
router.register(r'users', UsuarioViewSet, basename='usuario')
router.register(r'products', ProductoViewSet, basename='producto')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterViewSet.as_view(), name='register'),
]