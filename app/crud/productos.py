from sqlalchemy.orm import Session
from app.models.producto import Producto
from app.schemas.producto import ProductoCreate

#Funcion para crear un nuevo producto en la base de datos.
def crear_productos(db: Session, producto:ProductoCreate):
    db_producto = Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

# Funcion para obtener todos los productos de la base de datos.
def obtener_productos(db: Session):
    return db.query(Producto).all()

# Funcion para obtener un producto por su ID.
def obtener_producto(db: Session, producto_id: int):
    return db.query(Producto).filter(Producto.id == producto_id). first()

# Funcion para actualizar un producto existente en la base de datos.
def actualizar_productos(db: Session, producto_id: int, datos:ProductoCreate):
    producto = obtener_producto(db, producto_id)
    if producto:
        for key, value in datos.dict().items():
            setattr(producto, key, value)
        db.commit()
        db.refresh(producto)
    return producto

# funcion para eliminar un producto de la base de datos'
def eliminar_productos(db:Session, producto_id: int):
    producto = obtener_producto(db, producto_id)
    if producto:
        db.delete(producto)
        db.commit()
    return producto