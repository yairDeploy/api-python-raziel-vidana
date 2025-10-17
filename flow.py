import random
import requests
import json

BASE_URL = "http://ec2-13-59-82-32.us-east-2.compute.amazonaws.com/api"

def print_step(step_desc, response=None):
    print(f"\n\033[1;36m{step_desc}\033[0m")
    if response is not None:
        print(f"Status: {response.status_code}")
        try:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        except Exception:
            print("No JSON response.")

# --- PRODUCTO ---

def producto_creacion(headers):
    product_payload = {
        "nombre": "Producto API",
        "precio": 100.0,
        "stock": 10,
        "activo": True
    }
    print_step("Producto: Creación")
    resp = requests.post(f"{BASE_URL}/products/", json=product_payload, headers=headers)
    print_step("Producto: Creación (POST /products/)", resp)
    assert resp.status_code == 201
    return resp.json()["id"]

def producto_listado(headers):
    print_step("Producto: Listado")
    resp = requests.get(f"{BASE_URL}/products/", headers=headers)
    print_step("Producto: Listado (GET /products/)", resp)
    assert resp.status_code == 200
    return resp.json()

def producto_edicion(headers, producto_id):
    product_update = {
        "nombre": "Producto API Modificado",
        "precio": 150.0,
        "stock": 25,
        "activo": True
    }
    print_step("Producto: Edición")
    resp = requests.put(f"{BASE_URL}/products/{producto_id}/", json=product_update, headers=headers)
    print_step(f"Producto: Edición (PUT /products/{producto_id}/)", resp)
    assert resp.status_code == 200

def producto_detalle(headers, producto_id):
    print_step("Producto: Consulta única")
    resp = requests.get(f"{BASE_URL}/products/{producto_id}/", headers=headers)
    print_step(f"Producto: Consulta única (GET /products/{producto_id}/)", resp)
    assert resp.status_code == 200

def producto_eliminacion(headers, producto_id):
    print_step("Producto: Eliminación")
    resp = requests.delete(f"{BASE_URL}/products/{producto_id}/", headers=headers)
    print_step(f"Producto: Eliminación (DELETE /products/{producto_id}/)", resp)
    assert resp.status_code == 204

def producto_listado_post_eliminacion(headers, producto_id):
    print_step("Producto: Listado tras eliminación")
    resp = requests.get(f"{BASE_URL}/products/", headers=headers)
    print_step("Producto: Listado post-eliminación (GET /products/)", resp)
    assert resp.status_code == 200
    ids = [prod["id"] for prod in resp.json()]
    assert producto_id not in ids

# --- USUARIO ---

def usuario_creacion(headers):
    # Solo aquí se envía el password y será aceptado
    user_payload = {
        "username": f"nuevoflow_{random.randint(1000,9999)}",
        "nombre": "Nuevo",
        "apellido": "FlowUser",
        "edad": 29,
        "activo": True,
        "password": "UserPassword123"
    }
    print_step("Usuario: Creación")
    resp = requests.post(f"{BASE_URL}/users/", json=user_payload, headers=headers)
    print_step("Usuario: Creación (POST /users/)", resp)
    assert resp.status_code == 201
    return resp.json()["id"], user_payload["username"]

def usuario_listado(headers):
    print_step("Usuario: Listado")
    resp = requests.get(f"{BASE_URL}/users/", headers=headers)
    print_step("Usuario: Listado (GET /users/)", resp)
    assert resp.status_code == 200
    return resp.json()

def usuario_edicion(headers, usuario_id):
    # Aquí NO se envía el password
    user_update = {
        "username": f"edicionflow_{random.randint(1000,9999)}",
        "nombre": "Nuevo Mod",
        "apellido": "Modificado",
        "edad": 35,
        "activo": False
        # "password": "NoDeboEnviarEsto"   # <-- JAMÁS en edición
    }
    print_step("Usuario: Edición")
    resp = requests.put(f"{BASE_URL}/users/{usuario_id}/", json=user_update, headers=headers)
    print_step(f"Usuario: Edición (PUT /users/{usuario_id}/)", resp)
    assert resp.status_code == 200

def usuario_detalle(headers, usuario_id):
    print_step("Usuario: Consulta única")
    resp = requests.get(f"{BASE_URL}/users/{usuario_id}/", headers=headers)
    print_step(f"Usuario: Consulta única (GET /users/{usuario_id}/)", resp)
    assert resp.status_code == 200

def usuario_eliminacion(headers, usuario_id):
    print_step("Usuario: Eliminación")
    resp = requests.delete(f"{BASE_URL}/users/{usuario_id}/", headers=headers)
    print_step(f"Usuario: Eliminación (DELETE /users/{usuario_id}/)", resp)
    assert resp.status_code == 204

def usuario_listado_post_eliminacion(headers, username):
    print_step("Usuario: Listado tras eliminación")
    resp = requests.get(f"{BASE_URL}/users/", headers=headers)
    print_step("Usuario: Listado post-eliminación (GET /users/)", resp)
    assert resp.status_code == 200
    usernames = [u["username"] for u in resp.json()]
    assert username not in usernames

# --- MAIN FLOW ---

def main():
    numero_aleatorio = random.randint(1, 100)
    user_payload = {
        "username": f"testflow_{numero_aleatorio}",
        "nombre": f"Test {numero_aleatorio}",
        "apellido": f"Flow {numero_aleatorio}",
        "edad": 28,
        "activo": True,
        "password": "SuperSecret123"
    }

    print_step("1. Registro de usuario principal")
    resp = requests.post(f"{BASE_URL}/register/", json=user_payload)
    print_step("Respuesta registro:", resp)
    assert resp.status_code == 201

    login_payload = {
        "username": user_payload["username"],
        "password": user_payload["password"]
    }
    print_step("2. Obtención de token JWT")
    resp = requests.post(f"{BASE_URL}/token/", json=login_payload)
    print_step("Respuesta login/token:", resp)
    assert resp.status_code == 200
    token = resp.json()["access"]
    headers = {"Authorization": f"Bearer {token}"}

    print_step("=== FLUJO DE PRODUCTO ===")
    producto_id = producto_creacion(headers)
    producto_listado(headers)
    producto_edicion(headers, producto_id)
    producto_detalle(headers, producto_id)
    producto_eliminacion(headers, producto_id)
    producto_listado_post_eliminacion(headers, producto_id)

    print_step("=== FLUJO DE USUARIO ===")
    usuario_id, username = usuario_creacion(headers)
    usuario_listado(headers)
    usuario_edicion(headers, usuario_id)  # <-- password no se envía aquí
    usuario_detalle(headers, usuario_id)
    usuario_eliminacion(headers, usuario_id)
    usuario_listado_post_eliminacion(headers, username)

    print("\n\033[1;32m¡FLUJO DE PRUEBA DE PRODUCTO Y USUARIO COMPLETOS Y EXITOSOS!\033[0m")

if __name__ == "__main__":
    main()