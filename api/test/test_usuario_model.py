from django.test import TestCase
from django.utils import timezone
from api.models.usuario import Usuario

class UsuarioModelTest(TestCase):

    def test_crear_usuario(self):
        usuario = Usuario.objects.create_user(
            username='zpeda',
            password='superseguro',
            email='zpeda@ejemplo.com',
            edad=28,
            activo=True,
            first_name='Zulema',
            last_name='Pérez'
        )
        self.assertEqual(usuario.username, 'zpeda')
        self.assertEqual(usuario.email, 'zpeda@ejemplo.com')
        self.assertEqual(usuario.edad, 28)
        self.assertTrue(usuario.activo)
        self.assertTrue(usuario.is_active)  # De AbstractUser
        self.assertIsNotNone(usuario.created)
        self.assertIsNotNone(usuario.last_update)
        self.assertTrue(usuario.check_password('superseguro'))

    def test_valores_por_defecto(self):
        usuario = Usuario.objects.create_user(
            username='anon',
            password='clave123'
        )
        self.assertIsNone(usuario.edad)
        self.assertTrue(usuario.activo)  # Por defecto True

    def test_actualizar_last_update(self):
        usuario = Usuario.objects.create_user(username='edit', password='1234')
        anterior = usuario.last_update
        usuario.first_name = 'Edith'
        usuario.save()
        usuario.refresh_from_db()
        self.assertTrue(usuario.last_update >= anterior)

    def test_str_usuario(self):
        usuario = Usuario.objects.create_user(username='testuser', password='pass')
        self.assertEqual(str(usuario), 'testuser')  # Si defines __str__ como username
