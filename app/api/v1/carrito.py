from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import carrito as crud_carrito
from app.deps.deps import get_db, get_current_user

# Rutas para el carrito de compras.
api_router = APIRouter()

# Endpoint para ver el contenido del carrito.
@api_router.get("/", summary="Ver contenido del carrito")
def ver_carrito(db:Session = Depends(get_db), user = Depends(get_current_user)):
    carrito = crud_carrito.obtener_carrito(db, user.id)
    return carrito

# Endpoint para agregar un producto al carrito.
@api_router.post("/agregar/{producto_id}")
def agregar_producto(producto_id:int, cantidad: int = 1, db:Session = Depends(get_db), user=Depends(get_current_user)):
    carrito = crud_carrito.obtener_carrito(db, user.id)
    item = crud_carrito.agregar_item(db, carrito.id, producto_id, cantidad)
    return {"mensaje": "Producto agregado", "item": item}

# Endpoint para eliminar un producto del carrito.
@api_router.delete("/eliminar/{item_id}")
def eliminar_item(item_id: int, db:Session = Depends(get_db), user = Depends(get_current_user)):
    crud_carrito.eliminar_item(db, item_id)
    return {"mensaje": "Producto eliminado del carrito"}
