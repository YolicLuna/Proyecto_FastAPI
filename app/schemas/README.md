# Schemas - Documentación

Este directorio contiene los esquemas Pydantic que definen la validación y serialización de datos en la API. Los schemas actúan como intermediarios entre las solicitudes HTTP (JSON) y los modelos de base de datos (SQLAlchemy).

## Propósito de los Schemas

- **Validación:** Valida automáticamente los datos de entrada.
- **Serialización:** Convierte modelos ORM a JSON para respuestas.
- **Documentación:** Genera documentación automática en Swagger.
- **Type Hints:** Proporciona tipado seguro en toda la aplicación.
- **Seguridad:** Controla qué campos se exponen en las respuestas.

---

## Estructura de Archivos

### `categoria.py`
**Propósito:** Esquemas Pydantic para categorías de productos.

Define tres clases con diferentes niveles de exposición de datos.

**Estructura jerárquica:**
```
CategoriaBase.
    ↓
CategoriaCreate (hereda de CategoriaBase).
    ↓
CategoriaResponse (hereda de CategoriaBase).
```

#### `CategoriaBase`
- **Propósito:** Clase base con campos comunes.
- **Campos:**
  - `nombre: str` - Nombre de la categoría.
- **Uso:** Base para otras clases.

#### `CategoriaCreate`
- **Propósito:** Esquema para crear categorías.
- **Hereda:** `CategoriaBase`.
- **Campos adicionales:** Ninguno.
- **Validación:** Nombre es requerido.
- **Uso en endpoints:**
  ```python
  @app.post("/categorias")
  def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
      return crear_categorias(db, categoria)
  ```

#### `CategoriaResponse`
- **Propósito:** Esquema para respuestas de categorías.
- **Hereda:** `CategoriaBase`.
- **Campos adicionales:**
  - `id: int` - ID generado por la base de datos.
- **Configuración especial:**
  ```python
  class Config:
      from_attributes = True  # Permite trabajar con objetos ORM
  ```
- **Uso en endpoints:**
  ```python
  @app.get("/categorias", response_model=list[CategoriaResponse])
  def listar_categorias(db: Session = Depends(get_db)):
      return obtener_categorias(db)
  ```

**Ejemplo de flujo:**
```
Entrada JSON: {"nombre": "Electrónica"}
    ↓ (Validación CategoriaCreate)
CRUD crea en BD
    ↓
Modelo Categoria(id=1, nombre="Electrónica")
    ↓ (Serialización CategoriaResponse)
Salida JSON: {"id": 1, "nombre": "Electrónica"}
```

---

### `producto.py`
**Propósito:** Esquemas Pydantic para productos del catálogo.

Define dos clases para entrada y salida de datos de productos.

#### `ProductoCreate`
- **Propósito:** Esquema para crear productos.
- **Hereda:** `BaseModel` (no es base para ProductoResponse).
- **Campos requeridos:**
  - `nombre: str` - Nombre del producto.
  - `precio: float` - Precio del producto.
  - `en_stock: bool` - Disponibilidad en stock.
  - `categoria_id: int` - ID de la categoría.
- **Validación:**
  - `precio` debe ser número válido.
  - `categoria_id` debe existir en la base de datos.
- **Uso en endpoints:**
  ```python
  @app.post("/productos")
  def agregar_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
      return crear_productos(db, producto)
  ```

**Ejemplo de entrada:**
```json
{
    "nombre": "Laptop",
    "precio": 999.99,
    "en_stock": true,
    "categoria_id": 1
}
```

#### `ProductoResponse`
- **Propósito:** Esquema para respuestas de productos.
- **Hereda:** `ProductoCreate` (incluye todos sus campos).
- **Campos adicionales:**
  - `id: int` - ID del producto en la base de datos.
- **Configuración especial:**
  ```python
  class Config:
      from_attributes = True  # Convierte modelos ORM automáticamente
  ```
- **Uso en endpoints:**
  ```python
  @app.get("/productos/{id}", response_model=ProductoResponse)
  def obtener_producto(id: int, db: Session = Depends(get_db)):
      return obtener_producto(db, id)
  ```

**Ejemplo de salida:**
```json
{
    "id": 1,
    "nombre": "Laptop",
    "precio": 999.99,
    "en_stock": true,
    "categoria_id": 1
}
```

---

### `usuario.py`
**Propósito:** Esquemas Pydantic para gestión de usuarios y autenticación.

Define cuatro clases con diferentes niveles de exposición y propósitos.

**Estructura jerárquica:**
```
UsuarioBase
    ↓
UsuarioCreate (hereda de UsuarioBase)
    ↓
UsuarioResponse (hereda de UsuarioBase)

Token (independiente)
```

#### `UsuarioBase`
- **Propósito:** Clase base con campos públicos.
- **Campos:**
  - `nombre: str` - Nombre de usuario.
  - `email: EmailStr` - Email validado automáticamente por Pydantic.
- **Validación especial:**
  - Email debe ser válido (requiere instalación de `email-validator`).
- **Uso:** Base para otras clases.

#### `UsuarioCreate`
- **Propósito:** Esquema para registro de nuevos usuarios.
- **Hereda:** `UsuarioBase`.
- **Campos adicionales:**
  - `password: str` - Contraseña en texto plano (será hasheada en CRUD).
  - `es_admin: bool = False` - Indica si es administrador (opcional, por defecto False).
- **Validación:**
  - `nombre` - Requerido, debe ser único.
  - `email` - Requerido, debe ser válido y único.
  - `password` - Requerido, mínimo 8 caracteres (considerar agregar).
  - `es_admin` - Booleano con defecto.
- **Uso en endpoints:**
  ```python
  @app.post("/auth/usuarios", response_model=UsuarioResponse)
  def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
      return crear_usuarios(db, usuario)
  ```

**Ejemplo de entrada (registro):**
```json
{
    "nombre": "juan_perez",
    "email": "juan@example.com",
    "password": "micontraseña123",
    "es_admin": false
}
```

**⚠️ IMPORTANTE:** La contraseña nunca se retorna en respuestas por seguridad.

#### `UsuarioResponse`
- **Propósito:** Esquema para respuestas de usuario (perfil).
- **Hereda:** `UsuarioBase`.
- **Campos adicionales:**
  - `id: int` - ID del usuario.
  - `es_admin: bool` - Rol del usuario (sin defecto).
- **Campos NO incluidos:**
  - `password` - Por seguridad, nunca se expone.
  - `hashed_password` - Nunca se expone.
- **Configuración especial:**
  ```python
  class Config:
      from_attributes = True  # Convierte modelos ORM automáticamente
  ```
- **Uso en endpoints:**
  ```python
  @app.get("/auth/usuarios/me", response_model=UsuarioResponse)
  def obtener_perfil(current_user = Depends(get_current_user)):
      return current_user
  ```

**Ejemplo de salida (perfil):**
```json
{
    "id": 1,
    "nombre": "juan_perez",
    "email": "juan@example.com",
    "es_admin": false
}
```

#### `Token`
- **Propósito:** Esquema para respuesta de autenticación (login).
- **Hereda:** `BaseModel`.
- **Campos:**
  - `access_token: str` - Token JWT para autenticación.
  - `token_type: str = 'bearer'` - Tipo de token (por defecto: 'bearer').
- **Uso en endpoints:**
  ```python
  @app.post("/auth/login", response_model=Token)
  def login(form_data: OAuth2PasswordRequestForm = Depends(), ...):
      token = crear_token(...)
      return {'access_token': token, 'token_type': 'bearer'}
  ```

**Ejemplo de salida (login):**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

---

## Patrón de Herencia de Schemas.
El uso de clases base (como `CategoriaBase` y `UsuarioBase`) permite evitar la repetición de campos comunes y mantener una estructura clara. Las clases específicas (`Create`, `Response`) heredan de la base y agregan o modifican campos según el contexto (entrada vs salida).

---

## Configuración `from_attributes = True`

```python
class Config:
    from_attributes = True
```

**Propósito:** Permite a Pydantic convertir automáticamente objetos ORM (SQLAlchemy) a diccionarios/JSON.

**Sin esta configuración:**
```python
usuario_orm = db.query(Usuario).first()  # Objeto ORM
respuesta = UsuarioResponse(**usuario_orm)  # ❌ Error
```

**Con esta configuración:**
```python
usuario_orm = db.query(Usuario).first()  # Objeto ORM
respuesta = UsuarioResponse.model_validate(usuario_orm)  # ✅ Funciona
# O automáticamente en response_model=UsuarioResponse
```

---

## Validación de Datos

### Validación Automática de Pydantic

```python
# Email válido (EmailStr)
entrada = {"email": "usuario@example.com"}  # ✅ Válido

entrada = {"email": "email_invalido"}  # ❌ Error HTTP 422

# Tipos correctos
entrada = {"precio": 99.99}  # ✅ Correcto
entrada = {"precio": "no_numero"}  # ❌ Error HTTP 422

# Campos requeridos
entrada = {"nombre": "Producto"}  # ❌ Falta 'precio'
entrada = {"nombre": "Producto", "precio": 99.99}  # ✅ Correcto
```

### Respuestas de Error
```json
{
    "detail": [
        {
            "type": "value_error.email",
            "loc": ["body", "email"],
            "msg": "invalid email format",
            "input": "email_invalido"
        }
    ]
}
```

---

## Flujo Completo de Solicitud-Respuesta

### Ejemplo: Crear un Producto

```
1. Cliente envía JSON
   POST /productos
   {
       "nombre": "Laptop",
       "precio": 999.99,
       "en_stock": true,
       "categoria_id": 1
   }
        ↓
2. FastAPI valida con ProductoCreate
   ✓ nombre: str
   ✓ precio: float
   ✓ en_stock: bool
   ✓ categoria_id: int
        ↓
3. Endpoint recibe datos validados
   def agregar_producto(producto: ProductoCreate, ...)
        ↓
4. CRUD crea en BD
   db_producto = Producto(**producto.dict())
   db.add(db_producto)
   db.commit()
   db.refresh(db_producto)  # Obtiene el ID generado
        ↓
5. Objeto ORM se serializa con ProductoResponse
   {
       "id": 1,
       "nombre": "Laptop",
       "precio": 999.99,
       "en_stock": true,
       "categoria_id": 1
   }
        ↓
6. Cliente recibe respuesta JSON
   HTTP 200 OK
```

---

## Mejores Prácticas

### ✅ Hacer
- Usar `BaseModel` de Pydantic como clase base.
- Crear clases base para campos comunes.
- Usar `EmailStr` para validar emails.
- Usar `from_attributes = True` para modelos ORM.
- Validar tipos de datos automáticamente.
- No exponer campos sensibles (contraseñas, tokens internos).

### ❌ Evitar
- No mezclar Pydantic schemas con SQLAlchemy models.
- No validar manualmente lo que Pydantic puede hacer automáticamente.
- No retornar contraseñas en respuestas.
- No confundir Create/Response schemas (tienen propósitos diferentes).

---

## Resumen de Campos por Schema

| Schema | Campos | Propósito |
|--------|--------|----------|
| CategoriaCreate | nombre | Crear categoría |
| CategoriaResponse | id, nombre | Respuesta categoría |
| ProductoCreate | nombre, precio, en_stock, categoria_id | Crear producto |
| ProductoResponse | id, nombre, precio, en_stock, categoria_id | Respuesta producto |
| UsuarioCreate | nombre, email, password, es_admin | Registrar usuario |
| UsuarioResponse | id, nombre, email, es_admin | Perfil usuario |
| Token | access_token, token_type | Respuesta login |
