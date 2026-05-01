from fastapi import APIRouter,HTTPException, Depends
from sqlalchemy.orm import Session
from app.deps.deps import get_db, get_current_user
from crud import pedido as crud_pedido

router = APIRouter()

@router.post("/confirmar")
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

