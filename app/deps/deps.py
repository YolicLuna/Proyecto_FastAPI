from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session
from app.db.database import session_local
from deps import get_db
from app.core.security import verificar_token
import app.crud.usuario as usuario

# Configuración de OAuth2 para la autenticación de usuarios.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Función para obtener una sesión de la base de datos.
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

# Función para obtener el usuario actual a partir del token JWT proporcionado en la solicitud.
def get_current_user(
        token : str = Depends(oauth2_scheme),
        db:Session = Depends(get_db)
):
    # Excepción que se lanzará si el token no es válido o el usuario no existe.
    cred_exc = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail='No autenticado',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    # Verificar el token JWT y obtener su payload. Si el token no es válido, se lanzará la excepción de credenciales.
    try:
        payload = verificar_token(token)
        if payload is None:
            raise cred_exc
        email: str | None = payload.get('sub')
        if email is None:
            raise cred_exc
    except JWTError:
        raise cred_exc
    
    # Obtener el usuario de la base de datos utilizando el email extraído del token. 
    # Si el usuario no existe, se lanzará la excepción de credenciales.
    user = usuario.obtener_usuario_por_email(db, email)
    if user is None:
        raise cred_exc
    return user

# Función para verificar que el usuario actual tiene rol de admin. 
# Si no es así, se lanzará una excepción de autorización.
def require_admin(current_user= Depends(get_current_user)):
    if not current_user.es_admin:
        raise HTTPException(status_code=403, detail='No autorizado: se requiere rol admin')
    return current_user