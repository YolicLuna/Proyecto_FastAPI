from fastapi.testclient import TestClient
import os
import sys

# Se agrega el directorio raíz del proyecto al sys.path para poder importar el módulo main y acceder a la aplicación FastAPI. 
# Esto es necesario para que las pruebas puedan interactuar con la aplicación y realizar solicitudes HTTP a los endpoints
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Se importa la aplicación FastAPI desde el módulo main, 
# lo que permite que las pruebas puedan enviar solicitudes a los endpoints definidos en la aplicación.
from main import app

# Se crea un cliente de prueba utilizando TestClient, 
# que se utiliza para enviar solicitudes HTTP a la aplicación FastAPI durante las pruebas.
client = TestClient(app)

# Se define un token de autenticación válido para las pruebas, lo que permite que las pruebas puedan acceder a los endpoints protegidos por autenticación y autorización.
# El token se obtuvo mediante una solicitud de inicio de sesion con un administrador por medio de Insomnia, 
# y se utiliza en las pruebas para simular un usuario autenticado con privilegios de administrador.
token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtb29uZGV2QGVqZW1wbG8uY29tIiwiZXhwIjoxNzc4MDQzMjAyLCJlc19hZG1pbiI6dHJ1ZX0.A-d6tZTELRk5oidrscw4KD6a46aBbhPWUzCeKUPHGCA"

# Funcion de prueba para verificar la creación exitosa de un producto.
# Se envía una solicitud POST al endpoint de creación de productos con los datos necesarios, 
# y se verifica que la respuesta tenga un código de estado 200 
# y que los datos del producto creado coincidan con los datos enviados en la solicitud.
def test_crear_producto_exitoso():
    data = {
        "nombre": "Producto prueba",
        "precio": 20,
        "en_stock": True,
        "cantidad": 300,
        "categoria_id": 1
    }
    headers = {"Authorization": token}
    response = client.post("/api/v1/producto/productos", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json()["nombre"] == data["nombre"]
    assert response.json()["precio"] == data["precio"]

# Funcion de prueba para verificar la creación de un producto con datos faltantes,
# en este caso, se omite el campo "nombre" que es obligatorio.
# Se envía una solicitud POST al endpoint de creación de productos con los datos incompletos y se verifica que la respuesta tenga un código de estado 422,
# lo que indica que la solicitud no es válida debido a la falta de datos necesarios para crear el producto.
# Además, se verifica que el mensaje de error en la respuesta indique que el campo "nombre" es requerido.
def test_crear_producto_faltante_nombre():
    data = {
        "precio": 20,
        "en_stock": True,
        "cantidad": 300,
        "categoria_id": 1
    }
    headers = {"Authorization": token}
    response = client.post("/api/v1/producto/productos", json=data, headers=headers)
    assert response.status_code == 422
    assert "nombre" in response.text

# Funcion de prueba para verificar la lista de productos.
# Se envía una solicitud GET al endpoint de listado de productos y se verifica que la respuesta tenga un código de estado 200, lo que indica que la solicitud fue exitosa.
# Además, se verifica que la respuesta sea una lista, lo que indica que se han obtenido correctamente los productos disponibles en la base de datos.
def test_listar_productos():
    response = client.get("/api/v1/producto/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
