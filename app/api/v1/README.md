# API v1 - Documentación

Este directorio contiene los módulos principales de la API REST en su versión 1. Cada archivo organiza las rutas (endpoints) de forma modular para mantener el código limpio y escalable.

## Estructura de Archivos

### `api.py`
**Propósito:** Router principal de la API v1.

- Crea el router central que agrupa todos los módulos de la API.
- Incluye los routers específicos de cada módulo (`auth`, `productos`, `categorias`).
- Define los prefijos de ruta y etiquetas para organizar la documentación automática en Swagger.
- Actúa como punto de entrada para todas las rutas de la versión 1.

### `auth.py`
**Propósito:** Gestión de autenticación y autorización.

**Endpoints disponibles:**
- `POST /auth/usuarios` - Registrar un nuevo usuario.
- `POST /auth/login` - Iniciar sesión y obtener token JWT.
- `GET /auth/usuarios/me` - Obtener el perfil del usuario autenticado.
- `GET /auth/admin/ping` - Endpoint de prueba (requiere rol admin).

**Funcionalidades:**
- Registro de nuevos usuarios.
- Autenticación con correo y contraseña.
- Generación de tokens JWT.
- Validación de credenciales.
- Verificación de permisos de administrador.

### `categorias.py`
**Propósito:** Gestión de categorías de productos.

**Endpoints disponibles:**
- `GET /categorias/categorias` - Listar todas las categorías.
- `POST /categorias/categorias` - Crear una nueva categoría.

**Funcionalidades:**
- Visualizar todas las categorías disponibles.
- Crear nuevas categorías en el sistema.

### `productos.py`
**Propósito:** Gestión del catálogo de productos.

**Endpoints disponibles:**
- `GET /productos/productos` - Listar todos los productos.
- `POST /productos/productos` - Crear un nuevo producto (requiere rol admin).
- `PUT /productos/productos/{id}` - Actualizar un producto existente.
- `DELETE /productos/productos/{id}` - Eliminar un producto.

**Funcionalidades:**
- Visualizar el catálogo completo de productos.
- Crear productos (restringido a administradores).
- Actualizar información de productos.
- Eliminar productos del sistema.

## Patrones de Desarrollo

- **Dependency Injection:** Se utiliza `Depends()` de FastAPI para inyectar dependencias como sesiones de base de datos.
- **Autorización:** Los endpoints sensibles utilizan `require_admin` para validar permisos.
- **Validación:** Se usan Pydantic schemas para validar datos de entrada.
- **Manejo de Errores:** Se lanzan excepciones HTTP apropiadas (`HTTPException`) para casos de error.

## Estructura de Rutas

Todas las rutas siguen la estructura: `/v1/{modulo}/{endpoint}`

Ejemplo:
- `/v1/auth/login` - Login de usuario.
- `/v1/productos/productos` - Listar productos.
- `/v1/categorias/categorias` - Listar categorías.
