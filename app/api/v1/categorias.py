from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.categoria import CategoriaResponse, CategoriaCreate
from crud.categoria import * 
from app.deps.deps import get_db
from app.deps.deps import require_admin

api_router = APIRouter()

# Ruta para crear una nueva categoria.
@api_router.post("/categorias", response_model= CategoriaResponse)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    return crear_categorias(db, categoria)

# Ruta para listar todas las categorias.
@api_router.get("/categorias", response_model=list[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return obtener_categorias(db)