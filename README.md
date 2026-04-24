# FastAPI - API de Gestión de Productos y Categorías

## 📋 Descripción del Proyecto
API REST desarrollada con FastAPI para la gestión de productos, categorías y usuarios. El proyecto utiliza SQLAlchemy como ORM y MySQL como base de datos.

## ✨ Avances Realizados

### 1. **Configuración Base**
- ✅ Inicialización del proyecto con FastAPI
- ✅ Configuración de entorno virtual (venv)
- ✅ Instalación de dependencias principales
- ✅ Conexión a base de datos MySQL

### 2. **Modelos de Base de Datos** (`models.py`)
Se han creado tres modelos principales usando SQLAlchemy con relaciones bidireccionales y validaciones de integridad:

#### **Categorías** (`Categoria`)
```python
__tablename__ = 'categorias'
```
- `id`: Integer (clave primaria, indexado)
- `nombre`: String(50) - único e indexado
- `productos`: Relación one-to-many con `Producto` (back_populates='categorias')

**Validaciones:**
- Campo nombre único para evitar duplicados
- Index en nombre para optimizar búsquedas

#### **Productos** (`Producto`)
```python
__tablename__ = 'productos'
```
- `id`: Integer (clave primaria, indexado)
- `nombre`: String(50) - indexado
- `precio`: Float - valor numérico del producto
- `en_stock`: Boolean (por defecto: True) - estado de disponibilidad
- `categoria_id`: Integer - Clave foránea a `categorias.id`
- `categorias`: Relación many-to-one con `Categoria` (back_populates='productos')

**Características:**
- Index en nombre para búsquedas rápidas
- Relación con categoría para consultas relacionales
- Campo en_stock para control de inventario

#### **Usuarios** (`Usuario`)
```python
__tablename__ = 'usuarios'
```
- `id`: Integer (clave primaria, indexado)
- `nombre`: String(50) - único e indexado (identificador de usuario)
- `email`: String(50) - único e indexado (para contacto y autenticación)
- `hashed_password`: String(255) - almacena contraseña encriptada
- `es_admin`: Boolean (por defecto: False) - define permisos de administrador

**Características de Seguridad:**
- Campos nombre y email únicos e indexados
- Contraseña almacenada con hash (nunca en texto plano)
- Campo es_admin para control de roles y permisos
- Índices para optimizar búsquedas por email y nombre

**Características ORM Generales:**
- Relaciones bidireccionales configuradas con `back_populates` para navegación desde ambos lados
- Indexes en campos clave para optimizar búsquedas
- Constraints UNIQUE para garantizar integridad de datos
- Foreign keys para mantener consistencia referencial

### 3. **Funciones CRUD** (`crud.py`)
Se han implementado funciones de acceso a datos para productos, categorías y usuarios:

#### **Operaciones con Productos**
- `crear_producto(db, producto)` - Crear nuevo producto en la base de datos
- `obtener_productos(db)` - Obtener lista de todos los productos
- `obtener_producto(db, producto_id)` - Obtener un producto específico por ID
- `actualizar_producto(db, producto_id, datos)` - Actualizar datos de un producto existente
- `eliminar_producto(db, producto_id)` - Eliminar un producto de la base de datos

#### **Operaciones con Categorías**
- `crear_categoria(db, categoria)` - Crear nueva categoría en la base de datos
- `obtener_categorias(db)` - Obtener lista de todas las categorías

#### **Operaciones con Usuarios**
- **`obtener_usuario_por_email(db, email: str) → Usuario | None`**
  - Busca un usuario en la base de datos por su email
  - Retorna el objeto Usuario si existe, `None` si no

- **`obtener_usuario_por_id(db, usuario_id: int) → Usuario | None`**
  - Busca un usuario en la base de datos por su ID
  - Retorna el objeto Usuario si existe, `None` si no

- **`crear_usuario(db, usuario: UsuarioCreate) → Usuario`**
  - Crea nuevo usuario en la base de datos con validaciones de integridad
  - **Validación de duplicados:** Verifica que no exista otro usuario con el mismo email O nombre usando búsqueda OR
  - **Lanza excepción `ValueError`** si el usuario ya existe (mensaje: "Ya existe un usuario con ese email o nombre")
  - **Hashing de contraseña:** Aplica `hash_password()` a la contraseña antes de almacenarla
  - **Asignación de permisos:** Incluye el valor de `es_admin` del schema UsuarioCreate para definir permisos administrativos
  - **Transacciones:** Agrega el usuario, confirma cambios con commit y actualiza la instancia con refresh
  - Retorna el objeto Usuario creado con ID asignado por la base de datos

**Características de seguridad en usuarios:**
- Validación de duplicados mediante búsqueda OR en email y nombre antes de inserción
- Hash de contraseñas antes de almacenarlas (usando `hash_password()` de `utils.py` con bcrypt)
- Tipado de retorno con Union types (`Usuario | None`) para mayor claridad
- Manejo de excepciones explícito para intentos de creación duplicada
- Separación de responsabilidades: contraseña en texto plano recibida, hash aplicado antes de persistencia

### 4. **Configuración de Base de Datos** (`database.py`)
Módulo que gestiona la conexión y sesiones con la base de datos:

- **`DATABASE_URL`** - URL de conexión a MySQL con las credenciales configuradas
- **`engine`** - Motor SQLAlchemy que maneja la conexión a la base de datos
- **`session_local`** - Factory de sesiones configurable con:
  - `autocommit=False` - Requiere commit manual de transacciones
  - `autoflush=False` - Desactiva flush automático
  - `bind=engine` - Vincula el engine al sessionmaker
- **`Base`** - Clase base declarativa para todos los modelos ORM
- **`get_db()`** - Función dependency de FastAPI que proporciona sesiones de BD a los endpoints, garantizando cierre de conexión

### 5. **Endpoints API Implementados** (`main.py`)
API REST con validación de datos, manejo de errores y autenticación JWT:

#### **Gestión de Productos**
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/productos` | Listar todos los productos |
| POST | `/productos` | Crear nuevo producto |
| PUT | `/productos/{id}` | Actualizar producto existente |
| DELETE | `/productos/{id}` | Eliminar producto (retorna mensaje de confirmación) |

**Response Models:** Validación automática con `ProductoResponse`

#### **Gestión de Categorías**
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/categorias` | Listar todas las categorías |
| POST | `/categorias` | Crear nueva categoría |

**Response Models:** Validación automática con `CategoriaResponse`

#### **Gestión de Usuarios**
| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---|
| POST | `/usuarios` | Registrar nuevo usuario | No |
| POST | `/login` | Autenticarse y obtener token JWT | No (usa email/password) |
| GET | `/usuarios/me` | Obtener perfil del usuario autenticado | ✅ Required |

**Detalles de endpoints de usuarios:**

- **`POST /usuarios`** - Registrar nuevo usuario
  - **Schema:** `UsuarioCreate` (nombre, email, password, es_admin)
  - **Response:** `UsuarioResponse` con status 201 (Created)
  - **Validaciones:**
    - Email debe ser válido y único
    - Nombre debe ser único
    - Contraseña se hashea automáticamente
  - **Manejo de errores:** Retorna 400 si email o nombre ya existen

- **`POST /login`** - Autenticación y obtención de token JWT
  - **Formato:** `OAuth2PasswordRequestForm` (username, password)
  - **Parámetro username:** Se interpreta como email del usuario
  - **Validaciones:**
    - Verifica que el usuario exista por email
    - Verifica contraseña con `verify_password()` contra hash almacenado
  - **Response:** Token JWT con schema `Token` (access_token, token_type)
  - **Error 401:** Si credenciales son inválidas (usuario no existe o contraseña incorrecta)
  - **Token payload:** Incluye `sub` (email), `exp` (expiración), `es_admin` (permisos)

- **`GET /usuarios/me`** - Obtener perfil del usuario autenticado
  - **Autenticación:** ✅ Requerida (header `Authorization: Bearer <token>`)
  - **Dependencia:** `get_current_user` valida token y retorna usuario
  - **Response:** `UsuarioResponse` con datos del usuario autenticado
  - **Error 401:** Si token no es válido, expirado o no proporcionado

#### **Rutas de Prueba/Admin**
| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---|
| GET | `/admin/ping` | Endpoint de prueba para roles admin | ✅ Admin Required |

- **`GET /admin/ping`** - Verificar autenticación y permisos admin
  - **Autenticación:** ✅ Requerida (header `Authorization: Bearer <token>`)
  - **Autorización:** ✅ Requiere rol admin (`es_admin = True`)
  - **Dependencia:** `require_admin` valida token y permisos
  - **Response:** JSON con estado `{"ok": true, "role": "admin"}`
  - **Error 401:** Si token no es válido o no autenticado
  - **Error 403:** Si usuario autenticado NO tiene rol admin

**Características de seguridad implementadas:**
- Autenticación basada en tokens JWT con expiración (30 minutos)
- Autorización basada en roles (admin vs usuario regular)
- Contraseñas hasheadas con bcrypt antes de persistencia
- Validación automática de datos con Pydantic schemas
- Manejo de excepciones HTTP estándar (400, 401, 403, 404)
- Documentación automática en `/docs` (Swagger) y `/redoc`
- Validación de email automática (formato correcto y único)
- Headers OAuth2 estándar en respuestas de error

### 6. **Schemas de Validación** (`schemas.py`)
Modelos Pydantic para validación automática de datos de entrada/salida con soporte para validación de email y compatibilidad ORM:

#### **Productos**
- **`ProductoCreate`** - Schema para crear productos (usado en POST)
  - `nombre`: str - Nombre del producto
  - `precio`: float - Precio numérico del producto
  - `en_stock`: bool - Estado de disponibilidad (True/False)
  - `categoria_id`: int - ID de la categoría asociada (FK)
  - **Validaciones:** Tipos de datos automáticos

- **`ProductoResponse`** - Schema para respuestas de productos (usado en GET/PUT)
  - Hereda de `ProductoCreate` - Incluye todos los campos de ProductoCreate
  - `id`: int (añadido automáticamente por la base de datos)
  - `from_attributes = True` - Permite convertir objetos ORM de SQLAlchemy a diccionarios
  - **Uso:** Respuestas de endpoints GET, PUT, POST `/productos`

#### **Categorías**
- **`CategoriaBase`** - Schema base para categorías
  - `nombre`: str - Nombre de la categoría
  - **Propósito:** Reutilización común entre Create y Response

- **`CategoriaCreate`** - Schema para crear categorías (usado en POST)
  - Hereda de `CategoriaBase`
  - **Validaciones:** Tipo de datos (str)

- **`CategoriaResponse`** - Schema para respuestas de categorías (usado en GET/POST)
  - Hereda de `CategoriaBase`
  - `id`: int (añadido automáticamente por la base de datos)
  - `from_attributes = True` - Conversión de objetos ORM a diccionarios
  - **Uso:** Respuestas de endpoints GET, POST `/categorias`

#### **Usuarios**
- **`UsuarioBase`** - Schema base para usuarios
  - `nombre`: str - Nombre único del usuario
  - `email`: EmailStr - Email con validación de formato (RFC 5322)
  - **Propósito:** Campos comunes entre Create y Response

- **`UsuarioCreate`** - Schema para crear usuarios (usado en POST `/usuarios`)
  - Hereda de `UsuarioBase`
  - `password`: str - Contraseña en texto plano (será hasheada en CRUD antes de persistencia)
  - `es_admin`: bool (por defecto: False) - Flag de permisos administrativos
  - **Validaciones:** Email válido, tipos de datos correctos
  - **Nota:** La contraseña nunca se devuelve en respuestas

- **`UsuarioResponse`** - Schema para respuestas de usuarios (usado en GET/POST)
  - Hereda de `UsuarioBase`
  - `id`: int (añadido automáticamente por la base de datos)
  - `es_admin`: bool - Estado de permisos del usuario
  - `from_attributes = True` - Conversión de objetos ORM a diccionarios
  - **Nota:** No incluye `hashed_password` (campo sensible no expuesto en API)
  - **Uso:** Respuestas de endpoints POST `/usuarios`, GET `/usuarios/me`

#### **Autenticación**
- **`Token`** - Schema para respuesta de autenticación (usado en POST `/login`)
  - `access_token`: str - Token JWT codificado y firmado con SECRET_KEY
  - `token_type`: str (por defecto: 'bearer') - Tipo de token OAuth2 (siempre 'bearer' para JWT)
  - **Payload del token:** Contiene `sub` (email), `exp` (expiración), `es_admin`
  - **Uso:** Respuesta única del endpoint `/login` después de autenticación exitosa
  - **Cliente:** El token se envía en encabezado: `Authorization: Bearer <access_token>`

**Características de schemas en general:**
- **Validación automática:** Pydantic valida tipos de datos, formato de email, requeridos/opcionales
- **Serialización/deserialización JSON:** Conversión automática entre JSON y objetos Python
- **Validación de email:** `EmailStr` verifica formato RFC 5322 (estructura válida)
- **Compatibilidad ORM:** `from_attributes = True` (Pydantic v2) permite convertir objetos SQLAlchemy a dicts
- **Documentación automática:** Genera schemas en `/docs` (Swagger) y `/redoc`
- **Separación de responsabilidades:**
  - **Base:** Campos comunes (usado internamente)
  - **Create:** Para solicitudes de entrada (POST)
  - **Response:** Para salida de datos (GET, respuestas)
  - **Token:** Estructura específica de autenticación

**Patrones de uso en endpoints:**
```python
# POST /usuarios - entrada con UsuarioCreate, salida con UsuarioResponse
@app.post("/usuarios", response_model=schemas.UsuarioResponse)
def registrar(usuario: schemas.UsuarioCreate, ...):
    
# GET /usuarios/me - salida con UsuarioResponse
@app.get("/usuarios/me", response_model=schemas.UsuarioResponse)
def perfil(current_user = Depends(...)):
    
# POST /login - entrada con OAuth2PasswordRequestForm, salida con Token
@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(...)):
```

### 7. **Autenticación y Generación de Tokens** (`auth.py`)
Módulo para manejo de autenticación mediante tokens JWT:

#### **Configuración JWT**
```python
SECRET_KEY = 'clave_secreta'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```
- **`SECRET_KEY`** - Clave secreta para firmar y verificar tokens (⚠️ cambiar en producción)
- **`ALGORITHM`** - Algoritmo de criptografía usado para firmar tokens (HS256)
- **`ACCESS_TOKEN_EXPIRE_MINUTES`** - Duración de los tokens de acceso (30 minutos)

#### **Funciones de Autenticación**
- **`crear_token(sub: str, es_admin: bool) → str`**
  - Crea un token JWT con identificador de usuario y estado de administrador
  - Parámetro `sub` (subject): identificador único del usuario
  - Parámetro `es_admin`: indicador de permisos administrativos del usuario
  - Incluye automáticamente el timestamp de expiración (iat y exp)
  - El payload del token contiene: `sub`, `exp`, `es_admin`
  - Retorna el token codificado y firmado con la clave secreta

- **`verificar_token(token: str) → dict | None`**
  - Verifica y decodifica un token JWT
  - Retorna el payload completo si el token es válido
  - Retorna `None` si hay error en la verificación (token expirado, inválido o firmado incorrectamente)
  - Levanta excepción `JWSError` si el token tiene formato incorrecto

**Características de seguridad:**
- Tokens firmados digitalmente con clave secreta (HS256)
- Expiración automática de tokens después de 30 minutos
- Manejo de excepciones (`JWSError`) para tokens inválidos o expirados
- Payload decodificable para obtener información del usuario (sub, es_admin)
- Información de roles incluida directamente en el token para validaciones eficientes

### 8. **Dependencias y Validación de Autorización** (`deps.py`)
Módulo con funciones de dependencia para FastAPI que maneja autenticación y autorización:

#### **Configuración de OAuth2**
```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
```
- **`oauth2_scheme`** - Esquema de seguridad OAuth2 con contraseña portadora (Bearer tokens)
- Configura automáticamente la documentación de OpenAPI en `/docs`
- Extrae el token del encabezado `Authorization: Bearer <token>`

#### **Funciones de Dependencia**
- **`get_current_user(token: str, db: Session) → Usuario`**
  - Función de dependencia FastAPI que autentica la solicitud y retorna el usuario actual
  - **Validación de token:** Verifica que el token sea válido usando `verificar_token()`
  - **Extracción de identidad:** Obtiene el email (sub) del payload del token
  - **Manejo de errores:**
    - Retorna `HTTPException` con status 401 (UNAUTHORIZED) si:
      - Token no es válido o expirado
      - Payload no contiene el campo 'sub' (email)
      - Usuario no existe en la base de datos
    - Incluye encabezado `WWW-Authenticate: Bearer` en respuesta de error (estándar OAuth2)
  - **Retorno:** Objeto Usuario autenticado para uso en endpoints
  - **Uso en endpoints:** `@app.get("/ruta", dependencies=[Depends(get_current_user)])`

- **`require_admin(current_user: Usuario) → Usuario`**
  - Función de dependencia que valida permisos administrativos
  - **Validación:** Verifica que `current_user.es_admin == True`
  - Depende de `get_current_user` para obtener usuario autenticado
  - Retorna `HTTPException` con status 403 (FORBIDDEN) si el usuario NO es admin
  - Mensaje de error: "No autorizado: se requiere rol admin"
  - **Uso en endpoints:** `@app.delete("/admin/ruta", dependencies=[Depends(require_admin)])`

**Características de autorización:**
- Autenticación basada en tokens JWT con validación de integridad
- Autorización basada en roles (admin vs usuario regular)
- Composición de dependencias: `require_admin` depende de `get_current_user`
- Manejo de excepciones HTTP estándar (401, 403)
- Compatible con documentación automática de Swagger/OpenAPI
- Headers de autenticación OAuth2 estándar

### 9. **Funciones Utilitarias de Seguridad** (`utils.py`)
Módulo con funciones para manejo seguro de contraseñas usando bcrypt:

#### **Configuración de Hashing**
```python
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
```
- **`pwd_context`** - Contexto de criptografía configurado con bcrypt
- Algoritmo: bcrypt (estándar de la industria para hash de contraseñas)
- Parámetro `deprecated='auto'` - Permite actualizar automáticamente hashes antiguos

#### **Funciones de Seguridad**
- **`hash_password(password: str) → str`**
  - Genera un hash bcrypt de la contraseña proporcionada
  - La contraseña nunca se almacena en texto plano
  - Cada hash es único incluso para la misma contraseña (usa salt aleatorio)
  - Retorna el hash codificado listo para almacenar en BD

- **`verify_password(password: str, hashed: str) → bool`**
  - Verifica que una contraseña coincida con su hash almacenado
  - Retorna `True` si la contraseña es correcta
  - Retorna `False` si la contraseña es incorrecta
  - Resistente a ataques de timing

**Características de Seguridad:**
- Bcrypt con salt aleatorio para cada contraseña
- Imposible reversar el hash para obtener la contraseña original
- Función `verify_password()` resistente a timing attacks
- Compatible con esquemas de autenticación modernos
- Se puede usar salt personalizado si es necesario

### 10. **Scripts de Utilidad**
- ✅ `crear_tablas.py` - Script para crear todas las tablas en la base de datos automáticamente

### 11. **Dependencias Instaladas**
```
FastAPI
Uvicorn
PyMySQL
SQLAlchemy
Pydantic
python-jose (para JWT)
email-validator (para validación de emails)
passlib (para hashing de contraseñas)
bcrypt (algoritmo para passlib)
```

## 🛠️ Configuración Técnica

### Base de Datos
- **Sistema**: MySQL
- **Driver**: PyMySQL
- **URL de conexión**: `mysql+pymysql://root:contraseña@localhost:3306/api`
- **Puerto**: 3306
- **Usuario**: root
- **Host**: localhost
- **Base de datos**: api

### Entorno Virtual
- **Python**: 3.14.3+
- **Ubicación**: `./env/`
- **Gestor de paquetes**: pip

### Versiones de Dependencias
- FastAPI: 0.135.3+
- Uvicorn: 0.43.0+
- SQLAlchemy: 2.0.49+
- PyMySQL: 1.1.2+
- Pydantic: 2.12.5+
- python-jose: 3.3.0+ (para JWT)
- email-validator: 2.1.0+ (para validación de emails)
- passlib: 1.7.4+ (para hashing de contraseñas)
- bcrypt: 4.1.0+ (algoritmo de encriptación)

## 🚀 Cómo Usar

### Prerequisitos
- Python 3.14+
- MySQL Server ejecutándose
- Credenciales de acceso a la base de datos

### Pasos de Instalación y Ejecución

#### 1. Activar el entorno virtual
```powershell
.\env\Scripts\Activate.ps1
```

#### 2. Instalar o verificar dependencias (opcional)
```bash
pip install -r requirements.txt
```

#### 3. Crear las tablas en la base de datos
```bash
python app/crear_tablas.py
```
Este script creará automáticamente las tablas `categorias`, `productos` y `usuarios` en la base de datos.

#### 4. Ejecutar la API en modo desarrollo
```bash
uvicorn app.main:app --reload
```
O alternativamente:
```bash
python -m uvicorn app.main:app --reload
```

#### 5. Acceder a la API
- **URL Base**: `http://127.0.0.1:8000`
- **Swagger UI** (Documentación Interactiva): `http://127.0.0.1:8000/docs`
- **ReDoc** (Documentación Alternativa): `http://127.0.0.1:8000/redoc`

### Prueba rápida con curl
```bash
# Listar productos
curl http://127.0.0.1:8000/productos

# Listar categorías
curl http://127.0.0.1:8000/categorias

# Registrar nuevo usuario
curl -X POST http://127.0.0.1:8000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nombre":"usuario1","email":"user@example.com","password":"pass123","es_admin":false}'

# Iniciar sesión y obtener token
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=pass123"

# Obtener perfil del usuario autenticado (reemplazar TOKEN con el token obtenido)
curl http://127.0.0.1:8000/usuarios/me \
  -H "Authorization: Bearer TOKEN"

# Probar endpoint de admin
curl http://127.0.0.1:8000/admin/ping \
  -H "Authorization: Bearer TOKEN"
```

## 📁 Estructura del Proyecto
```
Proyecto_FastAPI/
├── app/
│   ├── main.py              # Endpoints de la API (recursos y rutas)
│   ├── models.py            # Modelos ORM de SQLAlchemy
│   ├── schemas.py           # Modelos Pydantic para validación
│   ├── crud.py              # Funciones CRUD de acceso a datos
│   ├── database.py          # Configuración de conexión a BD
│   ├── auth.py              # Autenticación y gestión de tokens JWT
│   ├── deps.py              # Dependencias FastAPI y validación de autorización
│   ├── utils.py             # Funciones utilitarias (hashing de contraseñas)
│   └── crear_tablas.py      # Script de inicialización de tablas
├── env/                     # Entorno virtual Python
├── requirements.txt         # Dependencias del proyecto
├── Data_base.sql           # Script SQL de referencia
├── LICENSE                 # Archivo de licencia
└── README.md               # Este archivo
```

## 📝 Próximos Pasos
- [x] Configuración base del proyecto con FastAPI
- [x] Modelos de base de datos con SQLAlchemy
- [x] Funciones CRUD para operaciones con BD
- [x] Endpoints para gestión de productos
- [x] Endpoints para gestión de categorías
- [x] Schemas de validación con Pydantic
- [x] Manejo de excepciones y errores
- [x] Implementar autenticación con JWT
- [x] Hashing de contraseñas con bcrypt/passlib
- [x] Schemas de usuarios (Create, Response, Base)
- [x] Funciones CRUD de usuarios
- [x] Módulo de autenticación y tokens JWT
- [x] Funciones de dependencia para autorización
- [x] Modelos de usuarios mejorados (es_admin)
- [x] Endpoints para gestión completa de usuarios (registro, login, perfil)
- [x] Sistema de roles y permisos basado en admin
- [x] Rutas protegidas con validación de tokens
- [ ] Validaciones adicionales (longitud mínima, formato, etc.)
- [ ] Refresh tokens para sesiones prolongadas
- [ ] Tests unitarios e integración
- [ ] Documentación de API mejorada
- [ ] Deployment a producción


## 👤 Autor
Desarrollado por: Proyecto en desarrollo

## 📄 Licencia
Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 💡 Notas Importantes
- Asegúrate de que MySQL Server esté ejecutándose antes de iniciar la API
- Actualiza las credenciales de base de datos en `app/database.py` según tu configuración local
- **SEGURIDAD**: Cambia `SECRET_KEY` en `app/auth.py` en producción (usar variable de entorno)
- **CONTRASEÑAS**: Nunca almacenes contraseñas en texto plano; usa `hash_password()` de `utils.py`
- La API usa SQLAlchemy 2.0 que requiere cambios en la forma de escribir consultas respecto a versiones anteriores
- Los modelos ORM automáticamente crean las relaciones inversas gracias a `back_populates`
- Bcrypt con passlib proporciona protección automática contra ataques timing en verificación de contraseñas
- Los tokens JWT expiran después de 30 minutos; requiere renovación para sesiones largas

## 🤝 Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias y mejoras.
