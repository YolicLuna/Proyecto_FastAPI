from fastapi import APIRouter,HTTPException, Depends
from sqlalchemy.orm import Session
from app.deps.deps import get_db, get_current_user
from app.crud import pedido as crud_pedido

# Rutas para el manejo de pedidos.
api_router = APIRouter()

# Endpoint para confirmar un pedido. 
# Crea un nuevo pedido para el usuario autenticado.
@api_router.post("/confirmar")
def confirmar_pedido(db:Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        pedido = crud_pedido.crear_pedido(db, user.id)
        return {
            "mensaje": "Pedido generado", 
            "pedido_id": pedido.id,
            "total": pedido.total
            }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

