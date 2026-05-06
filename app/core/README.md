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
**Propósito:** Funciones de seguridad y autenticación para la aplicación.

Proporciona utilidades para:
- Hashing seguro de contraseñas usando bcrypt.
- Validación de contraseñas.
- Generación de tokens JWT.
- Verificación y decodificación de tokens JWT.

**Configuración:**
- Contexto de hashing: Utiliza `bcrypt` como esquema para el hashing de contraseñas.
- Algoritmo JWT: Usa el algoritmo especificado en `config.py` (por defecto "HS256").

**Funciones principales:**

#### `hash_password(password: str) -> str`
- Realiza hash de una contraseña usando bcrypt.
- Utilizada para almacenar contraseñas de forma segura en la base de datos.
- Retorna el hash de la contraseña.

#### `verify_password(password: str, hashed: str) -> bool`
- Verifica que una contraseña coincida con su hash almacenado.
- Usada durante el login para validar credenciales.
- Retorna `True` si las contraseñas coinciden, `False` en caso contrario.

#### `crear_token(sub: str, es_admin: bool) -> str`
- Genera un token JWT con información del usuario.
- Parámetros:
  - `sub`: Correo electrónico del usuario (subject).
  - `es_admin`: Booleano indicando si el usuario tiene permisos de administrador.
- Incluye fecha de expiración basada en `ACCESS_TOKEN_EXPIRE_MINUTES`.
- Retorna el token JWT firmado y codificado.

#### `verificar_token(token: str) -> dict | None`
- Verifica y decodifica un token JWT.
- Retorna el payload del token si es válido.
- Retorna `None` si el token es inválido o ha expirado.
- Utiliza la clave secreta y algoritmo definidos en la configuración.

## Flujo de Seguridad

1. **Registro:** Se captura la contraseña → se realiza hash con `hash_password()` → se almacena en BD.
2. **Login:** Se verifica contraseña con `verify_password()` → si es válida, se genera token con `crear_token()` → se devuelve token.
3. **Acceso a recursos protegidos:** Se valida token con `verificar_token()` → se extrae información del usuario → se permite acceso.
4. **Almacenamiento de tokens:** Se usan en cabecera `Authorization: Bearer <token>`.

## Consideraciones de Seguridad

- **Algoritmo de hashing:** bcrypt (estándar de la industria).
- **Algoritmo JWT:** HS256 (HMAC con SHA-256).
- **Expiración:** Configurable a través de `ACCESS_TOKEN_EXPIRE_MINUTES` en el archivo `.env`.
- **Secret Key:** Debe ser una clave fuerte y secreta, almacenada en el archivo `.env`.
- **Payload del token:** Incluye `sub` (email), `es_admin` (rol) y `exp` (expiración).
