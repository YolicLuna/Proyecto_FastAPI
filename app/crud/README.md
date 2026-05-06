# CRUD - Documentación

Este directorio contiene las operaciones de **Create, Read, Update, Delete (CRUD)** para cada entidad del sistema. Estos módulos actúan como capa de acceso a datos, interactuando directamente con la base de datos a través de SQLAlchemy ORM. Cada archivo se enfoca en una entidad específica del negocio.

## Propósito de la Carpeta

La carpeta `crud` centraliza toda la lógica de operaciones de base de datos, siguiendo el patrón de arquitectura de capas. Esto permite:

- Separar la lógica de negocio de la lógica de acceso a datos.
- Reutilizar operaciones de base de datos desde diferentes endpoints de la API.
- Mantener un código limpio y fácil de mantener.
- Facilitar testing unitario de operaciones de base de datos.

## Estructura de Archivos

### `categoria.py`
Gestiona operaciones CRUD para categorías de productos. Permite crear nuevas categorías y recuperar todas las categorías disponibles del sistema. Las categorías se utilizan para clasificar y organizar el catálogo de productos.

### `productos.py`
Controla el ciclo de vida completo de los productos en el catálogo. Proporciona funcionalidades para crear nuevos productos, listar todos los disponibles, buscar productos individuales, actualizar información de productos existentes, y eliminar productos del sistema. Incluye validación de datos antes de realizar operaciones.

### `usuario.py`
Maneja operaciones relacionadas con usuarios del sistema. Permite crear nuevos usuarios con validación de duplicados (email y nombre único), buscar usuarios por email (utilizado en login) o por ID. Incluye hashing seguro de contraseñas durante el registro. Valida que no existan usuarios duplicados antes de crear nuevos.

### `carrito.py`
Gestiona las operaciones del carrito de compras asociado a cada usuario. Permite obtener o crear automáticamente un carrito para un usuario, agregar productos al carrito con manejo de cantidades, y eliminar items del carrito. Cuando un producto ya existe en el carrito, incrementa la cantidad en lugar de crear un duplicado.

### `pedido.py`
Convierte el carrito de compras en un pedido confirmado. Valida que el carrito no esté vacío, verifica disponibilidad de stock de los productos, calcula el total del pedido basado en precios y cantidades, actualiza el stock de productos, crea registros de detalles del pedido, y limpia el carrito después de confirmar el pedido. Maneja errores cuando hay problemas con el inventario.

## Patrones Utilizados

- **Inyección de dependencias:** Cada función recibe una sesión de base de datos como parámetro.
- **Validación de datos:** Se validan datos antes de realizar operaciones en la base de datos.
- **Manejo de transacciones:** Las operaciones se confirman (commit) después de modificaciones.
- **Type hints:** Uso de type hints de Python para mejor documentación y validación.
- **Reutilización:** Las funciones CRUD son llamadas desde los endpoints de la API y reutilizadas en diferentes contextos.
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
