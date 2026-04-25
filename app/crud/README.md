# CRUD - Documentación

Este directorio contiene las operaciones de **Create, Read, Update, Delete (CRUD)** para cada entidad del sistema. Estos módulos interactúan directamente con la base de datos a través de SQLAlchemy ORM.

## Estructura de Archivos

### `categoria.py`
**Propósito:** Operaciones CRUD para categorías de productos.

**Funciones disponibles:**

#### `crear_categorias(db: Session, categoria: CategoriaCreate) -> Categoria`
- Crea una nueva categoría en la base de datos.
- Parámetros:
  - `db` - Sesión de base de datos.
  - `categoria` - Schema de categoría con datos de entrada.
- Retorna la categoría creada con su ID asignado.
- Realiza commit automático en la base de datos.

#### `obtener_categorias(db: Session) -> list[Categoria]`
- Obtiene todas las categorías registradas en el sistema.
- Parámetros:
  - `db` - Sesión de base de datos.
- Retorna una lista de todas las categorías disponibles.

---

### `productos.py`
**Propósito:** Operaciones CRUD completas para el catálogo de productos.

**Funciones disponibles:**

#### `crear_productos(db: Session, producto: ProductoCreate) -> Producto`
- Crea un nuevo producto en la base de datos.
- Parámetros:
  - `db` - Sesión de base de datos.
  - `producto` - Schema de producto con datos de entrada.
- Retorna el producto creado con su ID asignado.
- Realiza commit automático.

#### `obtener_productos(db: Session) -> list[Producto]`
- Obtiene todos los productos del catálogo.
- Parámetros:
  - `db` - Sesión de base de datos.
- Retorna lista completa de productos.

#### `obtener_producto(db: Session, producto_id: int) -> Producto | None`
- Obtiene un producto específico por su ID.
- Parámetros:
  - `db` - Sesión de base de datos.
  - `producto_id` - ID del producto a buscar.
- Retorna el producto encontrado o `None` si no existe.

#### `actualizar_productos(db: Session, producto_id: int, datos: ProductoCreate) -> Producto | None`
- Actualiza los datos de un producto existente.
- Parámetros:
  - `db` - Sesión de base de datos.
  - `producto_id` - ID del producto a actualizar.
  - `datos` - Nuevos datos del producto.
- Retorna el producto actualizado o `None` si no existe.
- Realiza commit automático de los cambios.

#### `eliminar_productos(db: Session, producto_id: int) -> Producto | None`
- Elimina un producto de la base de datos.
- Parámetros:
  - `db` - Sesión de base de datos.
  - `producto_id` - ID del producto a eliminar.
- Retorna el producto eliminado o `None` si no existe.
- Realiza commit automático de la eliminación.

---

### `usuario.py`
**Propósito:** Operaciones CRUD para gestión de usuarios.

**Funciones disponibles:**

#### `obtener_usuario_por_email(db: Session, email: str) -> Usuario | None`
- Busca un usuario por su correo electrónico.
- Parámetros:
  - `db` - Sesión de base de datos.
  - `email` - Correo del usuario a buscar.
- Retorna el usuario encontrado o `None` si no existe.
- Utilizado durante el login y validación de duplicados.

#### `obtener_usuario_por_id(db: Session, usuario_id: int) -> Usuario | None`
- Busca un usuario por su ID.
- Parámetros:
  - `db` - Sesión de base de datos.
  - `usuario_id` - ID del usuario a buscar.
- Retorna el usuario encontrado o `None` si no existe.

#### `crear_usuarios(db: Session, usuario: UsuarioCreate) -> Usuario`
- Crea un nuevo usuario en la base de datos.
- Parámetros:
  - `db` - Sesión de base de datos.
  - `usuario` - Schema de usuario con datos de entrada.
- **Validaciones:**
  - Verifica que no exista otro usuario con el mismo email o nombre.
  - Lanza `ValueError` si el usuario ya existe.
- **Seguridad:**
  - Hashea la contraseña antes de almacenarla.
  - Utiliza la función `hash_password()` del módulo `core.security`.
- Retorna el usuario creado con su ID asignado.
- Realiza commit automático.

---

## Patrones y Convenciones

- **Inyección de Dependencias:** Todos los CRUD reciben una sesión (`Session`) como parámetro.
- **Transacciones:** Se utiliza `db.commit()` para confirmar cambios en la base de datos.
- **Refresh:** Se usa `db.refresh()` después de crear/actualizar para obtener datos actualizados del servidor.
- **Validación:** El CRUD de usuarios incluye validaciones de duplicados y hashing de contraseñas.
- **Seguridad:** Las contraseñas se hashean usando bcrypt antes de almacenarse.

## Uso Típico

```python
from app.crud.productos import crear_productos, obtener_productos
from app.deps.deps import get_db
from sqlalchemy.orm import Session

# En un endpoint
def listar_productos(db: Session = Depends(get_db)):
    productos = obtener_productos(db)
    return productos

# Crear un producto
def agregar_producto(datos: ProductoCreate, db: Session = Depends(get_db)):
    nuevo_producto = crear_productos(db, datos)
    return nuevo_producto
```
