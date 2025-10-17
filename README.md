# API Python Raziel Vidana

## Descripción

Esta es una API RESTful construida con Django 5, Django REST Framework, JWT (SimpleJWT), y MySQL. Incluye registro personalizado de usuarios, documentación Swagger con drf-yasg, y un entorno de desarrollo completo con Docker Compose.

---

## Decisiones técnicas importantes

### 1. **Base de datos**
- Se utiliza MySQL 8 como motor de base de datos.
- Las credenciales y configuración se gestionan mediante variables de entorno (`.env`), ideales para despliegue seguro y flexible.

### 2. **Modelo de usuario**
- El modelo de usuario es personalizado (`api.Usuario`), extendiendo el comportamiento estándar de Django.
- El registro de usuarios se realiza a través de un endpoint dedicado expuesto vía API REST.

### 3. **Autenticación**
- Se implementa autenticación JWT usando `djangorestframework-simplejwt`.
- El token se debe enviar en el header HTTP:
  ```
  Authorization: Bearer <access_token>
  ```
- **Access tokens** duran 5 minutos, **refresh tokens** 1 día (ver `SIMPLE_JWT` en `settings.py`).

### 4. **Documentación**
- La documentación OpenAPI/Swagger se genera automáticamente con drf-yasg.
- Endpoints:
  - Swagger UI: `/swagger/`
  - Redoc: `/redoc/`
- Nota: Los endpoints en Swagger aparecen sin el prefijo `/api/`, pero el acceso real es `/api/<ruta>`.

### 5. **Variables de entorno**
- Se utiliza un archivo `.env` para la configuración sensible y de entorno (base de datos, claves secretas, etc.).
- Docker Compose toma las variables directamente del `.env`.

### 6. **Contenedores**
- El entorno de desarrollo se administra con Docker Compose:
  - **web**: Django + API
  - **db**: MySQL
- El servicio web espera a que la base de datos MySQL esté lista antes de arrancar (healthcheck).

---

## Instalación y Uso

### 1. **Clonar el repositorio**
```bash
git clone https://github.com/yairDeploy/api-python-raziel-vidana
cd api-python-raziel-vidana
```

### 2. **Agregar permisos de ejecución al script inicial**
```bash
chmod +x entrypoint.sh
```

### 3. **Levantar los servicios**
```bash
docker-compose up --build
```

### 4. **Acceso a los servicios**
- **API Django**: [http://localhost:8000/api/](http://localhost:8000/api/)
- **Swagger**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **Redoc**: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

---

## Demo en producción

Puedes probar la API desplegada en AWS usando la siguiente URL base:

- **Demo URL:** [http://ec2-18-217-9-246.us-east-2.compute.amazonaws.com/api](http://ec2-18-217-9-246.us-east-2.compute.amazonaws.com/api)

Para documentación y pruebas interactivas:

- **Swagger (demo):** [http://ec2-18-217-9-246.us-east-2.compute.amazonaws.com/swagger/](http://ec2-18-217-9-246.us-east-2.compute.amazonaws.com/swagger/)
- **Redoc (demo):** [http://ec2-18-217-9-246.us-east-2.compute.amazonaws.com/redoc/](http://ec2-18-217-9-246.us-east-2.compute.amazonaws.com/redoc/)

---

## Probar los endpoints automáticamente

Hay un script de ejemplo llamado `flow.py` para probar los endpoints principales.

Primero, instala la dependencia necesaria:
```bash
pip install requests
```

Luego ejecuta el script:
```bash
python flow.py
```

---

## Endpoints principales

- `/api/register/` — Registro de usuarios (POST)
- `/api/token/` — Obtener access/refresh token JWT (POST)
- `/api/token/refresh/` — Refrescar access token JWT (POST)

### Usuarios
- `/api/users/` — Listado de usuarios (GET), Crear usuario (POST)
- `/api/users/{id}/` — Consultar usuario (GET), Actualizar usuario (PUT/PATCH), Eliminar usuario (DELETE)

### Productos
- `/api/products/` — Listado de productos (GET), Crear producto (POST)
- `/api/products/{id}/` — Consultar producto (GET), Actualizar producto (PUT/PATCH), Eliminar producto (DELETE)

---

## Notas adicionales

- La zona horaria está configurada como `America/Mexico_City`.
- El idioma principal es español mexicano (`es-mx`).

---

## Historial de commits

Consulta el historial estructurado de commits en el archivo [`historico_commits.txt`](./historico_commits.txt).

---

## Créditos

- Desarrollador principal: Raziel Vidana
- Contacto: razielyairdavila@gmail.com

---