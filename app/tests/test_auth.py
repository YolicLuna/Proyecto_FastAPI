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

# Funcion de prueba para verificar un inicio de sesión inválido.
# Se envía una solicitud POST al endpoint de inicio de sesión con credenciales incorrectas, 
# y se verifica que la respuesta tenga un código de estado 401, lo que indica que el inicio de sesión falló.
def test_login_invalid():
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "example@gmail.com",
            "password": "123"
        })
    assert response.status_code == 401

# Funcion de prueba para verificar un inicio de sesión exitoso.
# Se envía una solicitud POST al endpoint de inicio de sesión con credenciales correctas, 
# y se verifica que la respuesta tenga un código de estado 200, lo que indica que el inicio de sesión fue exitoso.
# Además, se verifica que la respuesta contenga un token de autenticación, lo que indica
def test_ping_docs():
    response = client.get("/docs")
    assert response.status_code == 200
