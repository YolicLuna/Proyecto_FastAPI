# API v1 - Documentación

Este directorio contiene los módulos principales de la API REST en su versión 1. Cada archivo organiza las rutas (endpoints) de forma modular para mantener el código limpio y escalable.

## Estructura de Archivos

### `api.py`
**Propósito:** Router principal de la API v1.

- Crea el router central que agrupa todos los módulos de la API.
- Incluye los routers específicos de cada módulo (`auth`, `productos`, `categorias`, `carrito`, `pedido`).
- Define los prefijos de ruta y etiquetas para organizar la documentación automática en Swagger.
- Actúa como punto de entrada para todas las rutas de la versión 1.

### `auth.py`
**Propósito:** Gestión de autenticación y autorización de usuarios.

**Endpoints disponibles:**
- `POST /v1/auth/usuarios` - Registrar un nuevo usuario.
- `POST /v1/auth/login` - Iniciar sesión y obtener token JWT.
- `GET /v1/auth/usuarios/me` - Obtener el perfil del usuario autenticado (requiere autenticación).
- `GET /v1/auth/admin/ping` - Endpoint de prueba (requiere rol admin).

**Funcionalidades:**
- Registro de nuevos usuarios con validación de email.
- Autenticación con correo y contraseña.
- Generación y validación de tokens JWT.
- Obtención del perfil del usuario autenticado.
- Verificación de permisos de administrador.

### `productos.py`
**Propósito:** Gestión del catálogo de productos.

**Endpoints disponibles:**
- `GET /v1/producto/` - Listar todos los productos.
- `POST /v1/producto/productos` - Crear un nuevo producto (requiere rol admin).
- `PUT /v1/producto/productos/{id}` - Actualizar un producto existente.
- `DELETE /v1/producto/productos/{id}` - Eliminar un producto.

**Funcionalidades:**
- Visualizar el catálogo completo de productos.
- Crear nuevos productos (restringido a administradores).
- Actualizar información de productos existentes.
- Eliminar productos del sistema.
- Validación de datos mediante Pydantic schemas.

### `categorias.py`
**Propósito:** Gestión de categorías de productos.

**Endpoints disponibles:**
- `GET /v1/categorias/categorias` - Listar todas las categorías.
- `POST /v1/categorias/categorias` - Crear una nueva categoría.

**Funcionalidades:**
- Visualizar todas las categorías disponibles.
- Crear nuevas categorías en el sistema.
- Validación de datos de entrada.

### `carrito.py`
**Propósito:** Gestión del carrito de compras de usuarios autenticados.

**Endpoints disponibles:**
- `GET /v1/carrito/` - Ver contenido del carrito del usuario autenticado.
- `POST /v1/carrito/agregar/{producto_id}` - Agregar un producto al carrito (parámetro opcional: cantidad).
- `DELETE /v1/carrito/eliminar/{item_id}` - Eliminar un producto del carrito.

**Funcionalidades:**
- Visualizar los items del carrito de compras.
- Agregar productos al carrito con cantidad especificada.
- Eliminar items del carrito.
- Validación de usuario autenticado.

### `pedido.py`
**Propósito:** Gestión de pedidos y confirmación de compras.

**Endpoints disponibles:**
- `POST /v1/pedido/confirmar` - Confirmar un pedido (convierte el carrito en pedido).

**Funcionalidades:**
- Crear nuevos pedidos basados en el carrito del usuario.
- Calcular el total del pedido automáticamente.
- Manejo de errores en caso de carrito vacío o problemas con el inventario.
- Respuesta con ID de pedido y total.

## Patrones de Desarrollo

- **Dependency Injection:** Se utiliza `Depends()` de FastAPI para inyectar dependencias como sesiones de base de datos y usuarios autenticados.
- **Autenticación:** Se utilizan tokens JWT para autenticar usuarios en endpoints protegidos.
- **Autorización:** Los endpoints sensibles utilizan `require_admin` para validar permisos de administrador.
- **Validación:** Se usan Pydantic schemas para validar datos de entrada (`UsuarioCreate`, `ProductoCreate`, `CategoriaCreate`).
- **Manejo de Errores:** Se lanzan excepciones HTTP apropiadas (`HTTPException`) con códigos de estado adecuados.
- **CRUD Operations:** Se delegan operaciones de base de datos a módulos específicos en `app.crud`.

## Estructura de Rutas

Todas las rutas siguen la estructura: `/v1/{modulo}/{endpoint}`

Ejemplos:
- `/v1/auth/login` - Login de usuario.
- `/v1/auth/usuarios/me` - Obtener perfil del usuario autenticado.
- `/v1/producto/` - Listar productos.
- `/v1/categorias/categorias` - Listar categorías.
- `/v1/carrito/` - Ver carrito.
- `/v1/pedido/confirmar` - Confirmar pedido.

## Seguridad

- **Endpoints protegidos:** Los endpoints que requieren autenticación utilizan `get_current_user` como dependencia.
- **Endpoints administrativos:** Algunos endpoints restrictos requieren `require_admin` para acceso.
- **Contraseñas:** Se utilizan funciones de hash seguras (`verify_password`) para validar credenciales.
- **Tokens JWT:** La autenticación se realiza mediante tokens JWT con información del usuario y su rol.
