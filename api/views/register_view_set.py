from rest_framework import generics
from django.contrib.auth import get_user_model
from api.serializers.register_serializer import RegisterSerializer

class RegisterViewSet(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []