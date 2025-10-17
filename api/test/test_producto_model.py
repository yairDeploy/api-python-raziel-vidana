from django.test import TestCase
from api.models.producto import Producto


class ProductoModelTest(TestCase):

    def test_crear_producto(self):
        producto = Producto.objects.create(
            nombre='Camiseta',
            precio=150.99,
            stock=25,
            activo=True
        )
        self.assertEqual(producto.nombre, 'Camiseta')
        self.assertEqual(producto.precio, 150.99)
        self.assertEqual(producto.stock, 25)
        self.assertTrue(producto.activo)
        self.assertIsInstance(producto, Producto)

    def test_valores_por_defecto(self):
        producto = Producto.objects.create(
            nombre='Gorra',
            precio=59.99
        )
        # stock y activo deben tomar los valores por defecto
        self.assertEqual(producto.stock, 0)
        self.assertTrue(producto.activo)

    def test_actualizar_producto(self):
        producto = Producto.objects.create(
            nombre='Bolso',
            precio=299.99,
            stock=5
        )
        producto.stock = 10
        producto.save()
        producto.refresh_from_db()
        self.assertEqual(producto.stock, 10)

    def test_str_producto(self):
        producto = Producto.objects.create(
            nombre='Zapatos',
            precio=199.99
        )
        self.assertEqual(str(producto), 'Zapatos')  # Si no tienes un método __str__, este test puede fallar o puedes quitarlo
