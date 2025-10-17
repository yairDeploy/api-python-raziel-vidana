from django.test import TestCase
from django.contrib.auth import get_user_model
from api.serializers.register_serializer import RegisterSerializer


Usuario = get_user_model()

class RegisterSerializerTest(TestCase):

    def setUp(self):
        self.valid_data = {
            'username': 'usuario_tester',
            'email': 'usuario@test.com',
            'first_name': 'Usuario',
            'last_name': 'Tester',
            'edad': 25,
            'password': 'passwordseguro'
        }

    def test_serializer_valid_data(self):
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        usuario = serializer.save()
        self.assertIsInstance(usuario, Usuario)
        self.assertEqual(usuario.username, self.valid_data['username'])
        self.assertTrue(usuario.check_password(self.valid_data['password']))
        self.assertEqual(usuario.edad, self.valid_data['edad'])
        self.assertEqual(usuario.email, self.valid_data['email'])

    def test_serializer_invalid_short_password(self):
        data = self.valid_data.copy()
        data['password'] = 'short'
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_serializer_missing_required_field(self):
        data = self.valid_data.copy()
        data.pop('username')
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_serializer_password_not_in_output(self):
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        usuario = serializer.save()
        output_data = RegisterSerializer(usuario).data
        self.assertNotIn('password', output_data)