from fastapi import FastAPI, Depends, HTTPException, status
from app.api.v1.api import api_router

# Crear la aplicación FastAPI.
# Se proporciona información adicional sobre la API, como el título, la descripción, la versión, la información de contacto y la licencia.
# Esto ayuda a documentar la API y proporciona detalles útiles para los desarrolladores que interactúan con ella.
app = FastAPI(
    title="E-commerce API",
    description="""
        API RESTful completa para la gestin de un E-commerce.

        Incluye:
        - Autenticacion con JWT.
        - Administracion de productos y categorias.
        - Carrito de compras.
        - Gestion de pedidos.
""",
version="1.0.0",

contact={
    "name": "José Yolic - Equipo Backend",
    "url": "git@github.com:YolicLuna/Proyecto_FastAPI.git",
    "email": "yolicdev@gmail.com"
},

license_info={
    "name": "MIT License",
    "url": "https://opensource.org/licences/MIT"
}

)

# Se incluye el router de la API con el prefijo "/api/v1" para organizar las rutas de la API bajo esa versión.
app.include_router(api_router, prefix="/api/v1")

# python -m uvicorn main:app --reload (Comando para correr el programa)
