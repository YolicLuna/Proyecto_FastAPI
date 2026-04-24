from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import app.crud.usuario as usuario, app.schemas as schemas
from app.deps.deps import get_db
from app.deps.deps import require_admin
from schemas.producto import ProductoCreate, ProductoResponse
from crud.productos import *

api_router = APIRouter()

# Ruta para listar todos los productos.
@api_router.get("/productos", response_model=list[ProductoResponse])
def listar_productos(db:Session = Depends(get_db)):
    return obtener_productos(db)

# Ruta para crear un nuevo producto.
@api_router.post("/productos", response_model=ProductoCreate, dependencies = [Depends(require_admin)])
def agregar_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    return crear_productos(db, producto)

# Ruta para actualizar un producto existente.
@api_router.put("/productos/{id}", response_model=ProductoCreate)
def actualizar_producto(producto_id: int, datos: ProductoCreate, db: Session = Depends(get_db)):
    producto = actualizar_productos(db, producto_id, datos)
    if not producto:
        raise HTTPException(status_code=404, detail='producto no encontrado')
    return producto

# Ruta para eliminar un producto.
@api_router.delete("/productos/{id}")
def eliminar_producto(producto_id: int, db:Session = Depends(get_db)):
    producto = eliminar_productos(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail='Producto no encontrado')
    return {'mensaje': 'Producto eliminado'}