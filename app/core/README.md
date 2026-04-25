# Core - Documentación

Este directorio contiene módulos esenciales para la configuración y seguridad de la aplicación. Incluye la gestión de variables de entorno y funciones criptográficas.

## Estructura de Archivos

### `config.py`
**Propósito:** Gestión centralizada de configuración de la aplicación.

- Utiliza `Pydantic BaseSettings` para cargar variables de entorno desde un archivo `.env`.
- Define una clase `Setting` que actúa como contenedor de configuración global.
- Proporciona validación automática de tipos para las variables de entorno.

**Variables de configuración:**
- `SECRET_KEY` - Clave secreta para firmar tokens JWT (requerida).
- `ALGORITHM` - Algoritmo utilizado para codificar JWT (por defecto: "HS256").
- `DATABASE_URL` - URL de conexión a la base de datos (requerida).
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Tiempo de expiración de tokens en minutos (requerido).

**Uso:**
```python
from app.core.config import setting
db_url = setting.DATABASE_URL
token_expiry = setting.ACCESS_TOKEN_EXPIRE_MINUTES
```

### `security.py`
**Propósito:** Funciones de seguridad y autenticación.

Proporciona utilidades para:
- Hashing de contraseñas.
- Validación de contraseñas.
- Generación de tokens JWT.
- Verificación de tokens JWT.

**Funciones principales:**

#### `hash_password(password: str) -> str`
- Realiza hash de una contraseña usando bcrypt.
- Utilizando para almacenar contraseñas de forma segura en la base de datos.
- Retorna el hash de la contraseña.

#### `verify_password(password: str, hashed: str) -> bool`
- Verifica que una contraseña coincida con su hash.
- Usada durante el login para validar credenciales.
- Retorna `True` si las contraseñas coinciden, `False` en caso contrario.

#### `crear_token(sub: str, es_admin: bool) -> str`
- Genera un token JWT con información del usuario.
- Incluye el correo del usuario (`sub`), estado de administrador (`es_admin`) y fecha de expiración.
- Firma el token usando `SECRET_KEY` y `ALGORITHM` de la configuración.
- Retorna el token JWT codificado.

#### `verificar_token(token: str) -> dict | None`
- Decodifica y verifica un token JWT.
- Retorna el payload del token si es válido.
- Retorna `None` si el token es inválido o ha expirado.

**Configuración de seguridad:**
- **Algoritmo de hashing:** bcrypt (estándar de la industria).
- **Algoritmo JWT:** HS256 (HMAC con SHA-256).
- **Expiración:** Configurable a través de `ACCESS_TOKEN_EXPIRE_MINUTES`.

## Flujo de Seguridad

1. **Registro:** La contraseña se hashea con `hash_password()` antes de almacenarse.
2. **Login:** Se verifica la contraseña con `verify_password()` y se genera un token con `crear_token()`.
3. **Autenticación:** Cada solicitud incluye el token, que se verifica con `verificar_token()`.
4. **Autorización:** El payload del token incluye el campo `es_admin` para control de acceso.
