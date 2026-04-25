# Deps - Documentación

Este directorio contiene las dependencias inyectables de FastAPI. Incluye funciones para gestionar sesiones de base de datos y validar autenticación y autorización de usuarios.

## Estructura de Archivos

### `deps.py`
**Propósito:** Dependencias inyectables para endpoints y manejo de autenticación.

Este archivo proporciona funciones reutilizables que se pueden inyectar en los endpoints usando `Depends()` de FastAPI.

---

## Componentes Principales

### `oauth2_scheme`
- Esquema de autenticación OAuth2 con bearers tokens.
- Especifica que los tokens se envían en el header `Authorization: Bearer <token>`.
- Dirección del endpoint de login: `tokenUrl='login'`.

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
```

**Uso en endpoints:**
```python
@app.get('/ruta-protegida')
def ruta(token: str = Depends(oauth2_scheme)):
    # El token se extrae automáticamente del header Authorization
    pass
```

---

## Funciones de Dependencia

### `get_db() -> Session`
**Propósito:** Proporcionar una sesión de base de datos a los endpoints.

- Crea una nueva sesión de base de datos usando `session_local()`.
- Garantiza que la sesión se cierre correctamente después de la solicitud.
- Utiliza `yield` para mantener la sesión abierta durante la ejecución del endpoint.

```python
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
```

**Uso en endpoints:**
```python
@app.get('/productos')
def listar_productos(db: Session = Depends(get_db)):
    return obtener_productos(db)
```

**Beneficios:**
- ✅ Abre la sesión solo cuando se necesita.
- ✅ Cierra la sesión automáticamente.
- ✅ Maneja excepciones correctamente.
- ✅ Evita fugas de conexión.

---

### `get_current_user(token: str, db: Session) -> Usuario`
**Propósito:** Obtener el usuario autenticado a partir del token JWT.

Realiza varios pasos de validación:

1. **Verificación del token**
   - Decodifica el token JWT usando `verificar_token()`.
   - Valida la firma del token.
   - Comprueba que el token no ha expirado.

2. **Extracción del email**
   - Obtiene el campo `sub` (subject) del payload del token.
   - Verifica que el email existe en el payload.

3. **Búsqueda en base de datos**
   - Busca el usuario por email en la base de datos.
   - Verifica que el usuario aún existe en el sistema.

**Excepciones lanzadas:**
- `HTTP 401 Unauthorized` - Si:
  - El token es inválido o ha expirado.
  - El token no contiene el email.
  - El usuario no existe en la base de datos.

**Ejemplo de uso:**
```python
@app.get('/usuarios/me', response_model=UsuarioResponse)
def obtener_perfil(current_user: Usuario = Depends(get_current_user)):
    return current_user
```

**Flujo de validación:**
```
Token enviado en header.
    ↓
Decodificar y verificar firma.
    ↓
Extraer email del payload.
    ↓
Buscar usuario en BD.
    ↓
Retornar usuario o lanzar excepción.
```

---

### `require_admin(current_user: Usuario) -> Usuario`
**Propósito:** Validar que el usuario autenticado tiene rol de administrador.

- Requiere un usuario autenticado (automáticamente valida el token).
- Verifica el campo `es_admin` del usuario.
- Lanza excepción si el usuario no es administrador.

**Excepciones lanzadas:**
- `HTTP 403 Forbidden` - Si el usuario no tiene rol admin.

**Ejemplo de uso:**
```python
@app.post('/productos', dependencies=[Depends(require_admin)])
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    return crear_productos(db, producto)
```

**Flujo de validación:**
```
Token enviado en header.
    ↓
Validar token con get_current_user().
    ↓
Verificar que es_admin = True.
    ↓
Si es admin: Retornar usuario.
Si no es admin: Lanzar HTTP 403.
```

---

## Cadena de Dependencias

Las dependencias se pueden anidar para crear flujos de validación más complejos:

```
Endpoint con require_admin.
    ↓
require_admin verifica si es admin.
    ↓
Internamente llama a get_current_user.
    ↓
get_current_user valida el token.
    ↓
Internamente llama a get_db.
    ↓
get_db proporciona sesión BD.
```

---

## Patrones de Seguridad

### 1. Endpoints Públicos (sin autenticación)
```python
@app.get('/productos')
def listar_productos(db: Session = Depends(get_db)):
    # Solo necesita BD, sin autenticación
    pass
```

### 2. Endpoints Protegidos (requieren autenticación)
```python
@app.get('/usuarios/me')
def perfil(current_user = Depends(get_current_user)):
    # Requiere token válido
    pass
```

### 3. Endpoints Restringidos (solo admin)
```python
@app.post('/productos')
def crear_producto(
    producto: ProductoCreate,
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    # Requiere token válido + rol admin
    pass
```

---

## Configuración Requerida

Para que las dependencias funcionen correctamente, es necesario:

1. **Variables de entorno** (en `.env`):
   - `SECRET_KEY` - Clave para firmar tokens.
   - `ALGORITHM` - Algoritmo de tokens (HS256).
   - `ACCESS_TOKEN_EXPIRE_MINUTES` - Expiración de tokens.
   - `DATABASE_URL` - URL de conexión a BD.

2. **Módulos importados correctamente**:
   - `app.db.database.session_local`.
   - `app.core.security.verificar_token`.
   - `app.crud.usuario`.

---

## Manejo de Errores

| Error | Causa | Solución |
|-------|-------|----------|
| HTTP 401 | Token inválido/expirado | Renovar token con login |
| HTTP 403 | Usuario no es admin | Usar cuenta de administrador |
| HTTP 422 | Token no incluido | Incluir header `Authorization: Bearer <token>` |
