from django.test import TestCase
from api.models.producto import Producto
from api.serializers.producto_serializer import ProductoSerializer

class ProductoSerializerTest(TestCase):
    def setUp(self):
        self.producto_data = {
            'nombre': 'Producto Test',
            'precio': 100.50,
            'stock': 10,
            'activo': True
        }
        self.producto = Producto.objects.create(**self.producto_data)

    def test_producto_serializer_valid_data(self):
        serializer = ProductoSerializer(instance=self.producto)
        data = serializer.data
        self.assertEqual(data['nombre'], self.producto_data['nombre'])
        self.assertEqual(float(data['precio']), float(self.producto_data['precio']))
        self.assertEqual(data['stock'], self.producto_data['stock'])
        self.assertEqual(data['activo'], self.producto_data['activo'])

    def test_producto_serializer_invalid_data(self):
        invalid_data = {
            'precio': 50,
            'stock': 5,
            'activo': True
        }
        serializer = ProductoSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('nombre', serializer.errors)

    def test_producto_serializer_create(self):
        data = {
            'nombre': 'Nuevo Producto',
            'precio': 200.00,
            'stock': 25,
            'activo': True
        }
        serializer = ProductoSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        producto = serializer.save()
        self.assertEqual(producto.nombre, data['nombre'])
        self.assertEqual(float(producto.precio), float(data['precio']))
        self.assertEqual(producto.stock, data['stock'])
        self.assertEqual(producto.activo, data['activo'])

    def test_precio_invalido(self):
        data = {
            'nombre': 'Producto inválido',
            'precio': 0.0,
            'stock': 5,
            'activo': True
        }
        serializer = ProductoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('precio', serializer.errors)
        self.assertEqual(serializer.errors['precio'][0], 'El precio debe ser mayor a 0.')

        data['precio'] = -8
        serializer = ProductoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('precio', serializer.errors)
        self.assertEqual(serializer.errors['precio'][0], 'El precio debe ser mayor a 0.')

    def test_stock_valido(self):
        data = {
            'nombre': 'Producto con stock cero',
            'precio': 10.0,
            'stock': 0,
            'activo': True
        }
        serializer = ProductoSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_stock_invalido(self):
        data = {
            'nombre': 'Producto con stock negativo',
            'precio': 10.0,
            'stock': -1,
            'activo': True
        }
        serializer = ProductoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('stock', serializer.errors)
        self.assertEqual(serializer.errors['stock'][0], 'El stock no puede ser negativo.')