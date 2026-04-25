from jose import JWSError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from.config import setting

# Configuración para el hashing de contraseñas utilizando bcrypt.
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Función para crear un token JWT a partir de un diccionario de datos.
def crear_token(sub:str, es_admin:bool):
    expire = datetime.utcnow() + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {
        'sub': sub,
        'exp': expire,
        'es_admin': es_admin
    }

    # Se genera el token JWT utilizando la clave secreta y el algoritmo especificados en la configuración.
    token = jwt.encode(data, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
    return token


# Función para verificar un token JWT y obtener su payload.
def verificar_token(token: str):
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        return payload
    except JWSError:
        return None

# Función para hashear una contraseña utilizando bcrypt.
def hash_password(password:str):
    return pwd_context.hash(password)

# Función para verificar una contraseña ingresada por el usuario contra su hash almacenado en la base de datos.
def verify_password(password:str, hashed: str):
    return pwd_context.verify(password, hashed)