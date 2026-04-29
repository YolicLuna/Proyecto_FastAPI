from sqlalchemy.orm import Session
from models.pedidos import Carrito, ItemCarrito

def obtener_carrito(db: Session, usuario_id: int):
    carrito = db.query(Carrito).filter(Carrito.usuarios_id == usuario_id).first()
    if not carrito:
        carrito = Carrito(usuario_id=usuario_id)
        db.add(carrito)
        db.commit()
        db.refresh(carrito)
    return carrito
