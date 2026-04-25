# Models - Documentación

Este directorio contiene los modelos de SQLAlchemy que definen la estructura de las tablas en la base de datos. Cada modelo representa una entidad del sistema y sus relaciones con otras entidades.

## Estructura de Archivos

### `categoria.py`
**Propósito:** Modelo de datos para categorías de productos.

Define la tabla `categorias` que almacena las categorías disponibles para clasificar productos.

**Definición de la clase:**
```python
class Categoria(Base):
    __tablename__ = 'categorias'
```

**Campos:**

| Campo | Tipo | Propiedades | Descripción |
|-------|------|-----------|-------------|
| `id` | Integer | Primary Key, Index | Identificador único de la categoría |
| `nombre` | String(50) | Unique, Index | Nombre de la categoría (único en el sistema) |
| `productos` | Relationship | - | Relación con tabla Producto (uno a muchos) |

**Relaciones:**
- **One-to-Many con Producto:** Una categoría puede tener muchos productos
- Especificado mediante `relationship('Producto', back_populates='categorias')`
- Permite acceder a todos los productos de una categoría: `categoria.productos`

**Ejemplo de uso:**
```python
# Crear una categoría
categoria = Categoria(nombre='Electrónica')

# Acceder a sus productos
productos_electronicos = categoria.productos
```

---

### `producto.py`
**Propósito:** Modelo de datos para productos del catálogo.

Define la tabla `productos` que almacena información del catálogo de productos.

**Definición de la clase:**
```python
class Producto(Base):
    __tablename__ = 'productos'
```

**Campos:**

| Campo | Tipo | Propiedades | Descripción |
|-------|------|-----------|-------------|
| `id` | Integer | Primary Key, Index | Identificador único del producto |
| `nombre` | String(50) | Index | Nombre del producto |
| `precio` | Float | - | Precio del producto |
| `en_stock` | Boolean | Default=True | Estado de disponibilidad (True = disponible) |
| `categoria_id` | Integer | Foreign Key → `categorias.id` | ID de la categoría a la que pertenece |
| `categorias` | Relationship | - | Relación con tabla Categoria (muchos a uno) |

**Relaciones:**
- **Many-to-One con Categoria:** Muchos productos pertenecen a una categoría
- Especificado mediante `relationship('Categoria', back_populates='productos')`.
- Permite acceder a la categoría del producto: `producto.categorias`.

**Restricciones:**
- El campo `categoria_id` es una clave foránea que referencia a `categorias.id`.
- No puede haber un producto sin categoría asignada.

**Ejemplo de uso:**
```python
# Crear un producto
producto = Producto(
    nombre='Laptop',
    precio=999.99,
    en_stock=True,
    categoria_id=1
)

# Acceder a su categoría
categoria = producto.categorias
```

---

### `usuario.py`
**Propósito:** Modelo de datos para usuarios del sistema.

Define la tabla `usuarios` que almacena información de autenticación y autorización.

**Definición de la clase:**
```python
class Usuario(Base):
    __tablename__ = 'usuarios'
```

**Campos:**

| Campo | Tipo | Propiedades | Descripción |
|-------|------|-----------|-------------|
| `id` | Integer | Primary Key, Index | Identificador único del usuario |
| `nombre` | String(50) | Unique, Index | Nombre de usuario (único en el sistema) |
| `email` | String(50) | Unique, Index | Correo electrónico (único en el sistema) |
| `hashed_password` | String(255) | - | Contraseña hasheada con bcrypt |
| `es_admin` | Boolean | Default=False | Indica si el usuario tiene permisos de administrador |

**Restricciones:**
- `nombre` debe ser único.
- `email` debe ser único.
- `hashed_password` siempre debe estar hasheada (nunca en texto plano).
- `es_admin` por defecto es `False` (usuarios regulares).

**Campos que nunca se retornan en respuestas:**
- `hashed_password` - Por seguridad, nunca se expone en las respuestas API.

**Ejemplo de uso:**
```python
# Crear un usuario
usuario = Usuario(
    nombre='juan_perez',
    email='juan@example.com',
    hashed_password=hash_password('mi_contraseña'),
    es_admin=False
)

# Verificar si es admin
if usuario.es_admin:
    # Usuario tiene permisos de administrador
    pass
```

---

## Patrón de Herencia

Todos los modelos heredan de `Base`, que es la clase base declarativa de SQLAlchemy:

```python
from app.db.database import Base

class MiModelo(Base):
    __tablename__ = 'nombre_tabla'
    # ... campos
```

**Beneficios:**
- SQLAlchemy registra automáticamente todos los modelos en `Base.metadata`.
- Facilita la creación automática de tablas con `Base.metadata.create_all()`.
- Proporciona funcionalidad ORM estándar (queries, inserts, updates, deletes).

---

## Indexing

Se utilizan índices para optimizar consultas:

**Campos indexados:**
- `Categoria.id` - Primary key (automáticamente indexado).
- `Categoria.nombre` - Para búsquedas por nombre.
- `Producto.id` - Primary key.
- `Producto.nombre` - Para búsquedas por nombre.
- `Usuario.id` - Primary key.
- `Usuario.nombre` - Para búsquedas por nombre.
- `Usuario.email` - Para búsquedas por email.

**Campos con UNIQUE constraint:**
- `Categoria.nombre` - No puede haber dos categorías con el mismo nombre.
- `Producto.nombre` - (implícitamente, según el índice).
- `Usuario.nombre` - No puede haber dos usuarios con el mismo nombre.
- `Usuario.email` - No puede haber dos usuarios con el mismo email.

---

## Ciclo de Vida de los Modelos

### 1. Definición
Los modelos se definen en este directorio heredando de `Base`.

### 2. Registro en SQLAlchemy
Al importar los modelos, SQLAlchemy los registra automáticamente en `Base.metadata`.

### 3. Creación de Tablas
Se ejecuta `init_db.py` para crear las tablas en la base de datos.

### 4. Operaciones CRUD
Los CRUD en `/crud` utilizan estos modelos para realizar consultas.

### 5. Serialización en Schemas
Los modelos se convierten en respuestas JSON usando schemas en `/schemas`.

---

## Uso en la Aplicación

### En CRUD (Lectura/Escritura):
```python
from app.models.usuario import Usuario
from sqlalchemy.orm import Session

def obtener_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()
```

### En Endpoints:
```python
from app.models.producto import Producto

@app.get('/productos/{id}')
def obtener_producto(id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == id).first()
    return producto
```

### Acceso a Relaciones:
```python
# Obtener todos los productos de una categoría
categoria = db.query(Categoria).filter(Categoria.id == 1).first()
productos = categoria.productos  # Lazy loading

# Obtener la categoría de un producto
producto = db.query(Producto).filter(Producto.id == 1).first()
categoria = producto.categorias
```

---

## Consideraciones de Seguridad

1. **Contraseñas:** Siempre hasheadas en el campo `hashed_password`.
2. **Unicidad:** Los campos únicos previenen duplicados en el sistema.
3. **Autorización:** El campo `es_admin` controla el acceso a operaciones sensibles.
4. **Indices:** Optimizan consultas de búsqueda sin sacrificar seguridad.
