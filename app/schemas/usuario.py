from pydantic import BaseModel, EmailStr

# Clases para el usuario, con validación de email y campos necesarios para la creación y respuesta.
class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr

# Clase para la creación de un usuario, que incluye la contraseña y el campo para indicar si es administrador.
class UsuarioCreate(UsuarioBase):
    password: str
    es_admin: bool = False

# Clase de respuesta para el usuario, que incluye el ID generado por la base de datos y el campo para indicar si es administrador.
class UsuarioResponse(UsuarioBase):
    id: int
    es_admin : bool
    # Configuración para que Pydantic pueda trabajar con objetos ORM de SQLAlchemy.
    class Config:
        from_attributes = True

# Clase para la respuesta del token JWT, que incluye el token de acceso y el tipo de token.
class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'