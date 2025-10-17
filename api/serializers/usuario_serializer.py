from rest_framework import serializers
from api.models.usuario import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='first_name')
    apellido = serializers.CharField(source='last_name')
    activo = serializers.BooleanField(source='is_active')

    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'nombre', 'apellido', 'edad', 'activo',
            'created', 'last_update'
        ]
        read_only_fields = ['id', 'created', 'last_update']

    def validate_edad(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("La edad no puede ser negativa.")
        return value

    def create(self, validated_data):
        # Solo en la creación pedimos el password
        password = self.initial_data.get('password')
        usuario = super().create(validated_data)
        if password:
            usuario.set_password(password)
            usuario.save()
        return usuario

    def to_internal_value(self, data):
        # Solo acepta password en create, lo elimina en otros casos
        ret = super().to_internal_value(data)
        # Si no es creación, eliminamos password del diccionario para evitar problemas
        if self.instance is not None and 'password' in ret:
            ret.pop('password')
        return ret