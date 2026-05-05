from sqlalchemy.orm import Session
from app.models.producto import Producto
from app.models.pedidos import Carrito, DetallePedido, Pedido

# Funcion para crear un pedido a partir del carrito de un usuario.
def crear_pedido(db:Session, usuario_id: int):
    carrito = db.query(Carrito).filter_by(usuarios_id=usuario_id).first()
    if not carrito or not carrito.items:
        raise ValueError("El carrito esta vacio")
    
    total = 0
    pedido = Pedido(usuario_id=usuario_id, total=0)
    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    # Recorremos los items del carrito para crear los detalles del pedido y actualizar el stock de los productos.
    for item in carrito.items:
        producto = db.query(Producto).filter(Producto.id == item.producto_id).first()
        if producto is None or producto.en_stock is False or producto.precio <= 0:
            continue
        
        # Validamos que la cantidad solicitada sea mayor a 0 y menor o igual al stock disponible.
        if item.cantidad > 0 and item.cantidad <= (producto.stock or 0):
            producto.stock -= item.cantidad
            subtotal = producto.precio * item.cantidad
            detalle = DetallePedido(
                pedido_id = pedido.id,
                producto_id = producto.id,
                cantidad = item.cantidad,
                subtotal = subtotal
            )
            # Agregamos el detalle del pedido a la base de datos y acumulamos el total del pedido.
            db.add(detalle)
            total += subtotal
    # Actualizamos el total del pedido y guardamos los cambios en la base de datos.
    pedido.total = total
    db.commit()
    for item in carrito.items:
        db.delete(item)
    db.commit()
    return pedido
