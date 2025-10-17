from rest_framework import serializers
from api.models.usuario import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='first_name')
    apellido = serializers.CharField(source='last_name')
    activo = serializers.BooleanField(source='is_active')

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'nombre', 'apellido', 'edad', 'activo', 'created', 'last_update']
        read_only_fields = ['id', 'created', 'last_update']