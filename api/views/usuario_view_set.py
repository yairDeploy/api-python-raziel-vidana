from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.models.usuario import Usuario
from api.serializers.usuario_serializer import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

