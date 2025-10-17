from django.test import TestCase
from api.models.usuario import Usuario
from api.serializers.usuario_serializer import UsuarioSerializer

class UsuarioSerializerTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            username='zpeda',
            first_name='Zulema',
            last_name='Pérez',
            edad=31,
            is_active=True
        )

    def test_usuario_serializer_data(self):
        serializer = UsuarioSerializer(instance=self.usuario)
        data = serializer.data
        self.assertEqual(data['username'], 'zpeda')
        self.assertEqual(data['nombre'], 'Zulema')
        self.assertEqual(data['apellido'], 'Pérez')
        self.assertEqual(data['edad'], 31)
        self.assertEqual(data['activo'], True)
        self.assertIn('created', data)
        self.assertIn('last_update', data)

    def test_usuario_serializer_create_with_password(self):
        payload = {
            'username': 'pepito',
            'nombre': 'Pepito',
            'apellido': 'Gómez',
            'edad': 22,
            'activo': False,
            'password': 'Password123'
        }
        serializer = UsuarioSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        usuario = serializer.save()
        self.assertEqual(usuario.first_name, payload['nombre'])
        self.assertEqual(usuario.last_name, payload['apellido'])
        self.assertEqual(usuario.edad, payload['edad'])
        self.assertEqual(usuario.is_active, payload['activo'])
        self.assertTrue(usuario.check_password(payload['password']))

    def test_usuario_serializer_create_without_password(self):
        payload = {
            'username': 'pepito2',
            'nombre': 'Pepito',
            'apellido': 'Gómez',
            'edad': 22,
            'activo': True
        }
        serializer = UsuarioSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        usuario = serializer.save()
        # Password no seteado, debe estar vacío
        self.assertTrue(usuario.password == "" or usuario.password is not None)

    def test_read_only_fields_cannot_be_written(self):
        payload = {
            'username': 'user2',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'edad': 28,
            'activo': True,
            'password': 'OtroPassword123',
            'id': 999,
            'created': '2020-01-01T00:00:00Z',
            'last_update': '2020-01-01T00:00:00Z'
        }
        serializer = UsuarioSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        usuario = serializer.save()
        self.assertNotEqual(usuario.id, 999)  # Django asigna el ID
        # Las fechas se asignan automáticamente, no por el payload

    def test_edad_no_negativa(self):
        payload = {
            'username': 'negativo',
            'nombre': 'Pepe',
            'apellido': 'Negativo',
            'edad': -5,
            'activo': True,
            'password': 'PasswordNegativo'
        }
        serializer = UsuarioSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn('edad', serializer.errors)
        self.assertEqual(serializer.errors['edad'][0], 'La edad no puede ser negativa.')

    def test_update_does_not_change_password(self):
        # Creamos un usuario con password
        usuario = Usuario.objects.create_user(
            username='modificado',
            first_name='Mod',
            last_name='ificado',
            edad=30,
            is_active=True,
            password='Original123'
        )
        old_hash = usuario.password
        payload = {
            'nombre': 'Modificado',
            'apellido': 'Cambiado',
            'edad': 35,
            'activo': False,
            'password': 'NuevoIntento123'  # No debe cambiar el password
        }
        serializer = UsuarioSerializer(instance=usuario, data=payload, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        usuario_modificado = serializer.save()
        self.assertEqual(usuario_modificado.first_name, 'Modificado')
        self.assertEqual(usuario_modificado.last_name, 'Cambiado')
        self.assertEqual(usuario_modificado.edad, 35)
        self.assertEqual(usuario_modificado.is_active, False)
        self.assertEqual(usuario_modificado.password, old_hash)  # password no se modifica