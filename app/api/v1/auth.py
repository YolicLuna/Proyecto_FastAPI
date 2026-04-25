from fastapi import Depends, HTTPException, status
from app.deps.deps import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import crear_token, verify_password
from deps.deps import get_current_user, require_admin
from schemas.usuario import UsuarioResponse, UsuarioCreate
from crud.usuario import obtener_usuario_por_email, crear_usuarios
from fastapi import APIRouter
from typing import cast

# Se crea un router específico para las rutas de autenticación, 
# lo que permite organizar mejor el código y separar las responsabilidades.
api_router = APIRouter ()

# Ruta para registrar un nuevo usuario.
@api_router.post('/usuarios', response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate, db:Session = Depends(get_db)):
    try:
        return crear_usuarios(db, usuario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Ruta para iniciar sesión y obtener un token JWT. 
@api_router.post('/login', response_model=UsuarioResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = obtener_usuario_por_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail='Credenciales invalidas')
    
    hashed_password: str = cast(str, user.hashed_password)
    if not verify_password(form_data.password, hashed_password):
        raise HTTPException(status_code=401, detail='Credenciales invalidas')
    
    email: str = cast(str, user.email)
    es_admin: bool = cast(bool, user.es_admin)
    token = crear_token(sub=email, es_admin=es_admin)
    return {'access_token': token, 'token_type': 'bearer'}

# Ruta para obtener el perfil del usuario autenticado.
@api_router.get('/usuarios/me', response_model=UsuarioResponse)
def leer_perfil(current_user = Depends(get_current_user)):
    return current_user

# Ruta de prueba para verificar que la autenticación funciona correctamente.
@api_router.get('/admin/ping')
def admin_ping(_admin = Depends(require_admin)):
    return {'ok': True, 'role': 'admin'}