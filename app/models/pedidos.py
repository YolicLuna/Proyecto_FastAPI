from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

# Clases para el carrito de compras y pedidos.
class Carrito(Base):
    __tablename__ = "carritos"
    id = Column(Integer, primary_key=True, index=True)
    usuarios_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="carrito")
    items = relationship("ItemCarrito", back_populates="carrito", cascade="all, delete")

# Clase para representar los productos en el carrito de compras.
class ItemCarrito(Base):
    __tablename__ = "item_carrito"
    id = Column(Integer, primary_key=True, index=True)
    carrito_id = Column(Integer, ForeignKey("carritos.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, default=1)
    carrito = relationship("Carrito", back_populates="items")
    producto = relationship("Producto")

# Clases para representar los pedidos realizados por los usuarios.
class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha = Column(DateTime, default=datetime.now)
    total = Column(Float)
    detalle = relationship("DetallePedido", back_populates="pedido")

# Clase para representar los detalles de cada pedido, incluyendo los productos y cantidades.
class DetallePedido(Base):
    __tablename__ = "detalles_pedidos"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer)
    subtotal = Column(Float)
    pedido = relationship("Pedido", back_populates="detalle")
    producto = relationship("Producto")
