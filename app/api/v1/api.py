from fastapi import APIRouter
from app.api.v1 import auth, productos, categorias, carrito, pedido

# Se crea un router principal para la versión 1 de la API.
api_router = APIRouter()

# Se incluyen los routers específicos de cada módulo (auth, productos, categorias, carrito y pedido) con sus respectivos prefijos y etiquetas,
# para organizar mejor la API y facilitar su mantenimiento. 
# Esto permite que cada módulo tenga su propio conjunto de rutas, 
# mientras que el router principal se encarga de agruparlas bajo la versión 1 de la API.
api_router.include_router(auth.api_router, prefix="/auth", tags=["auth"])
api_router.include_router(productos.api_router, prefix="/producto", tags=["productos"])
api_router.include_router(categorias.api_router, prefix="/categorias", tags=["categorias"])
api_router.include_router(carrito.api_router, prefix="/carrito", tags=["carritos"])
api_router.include_router(pedido.api_router, prefix="/pedido", tags=["pedidos"])

