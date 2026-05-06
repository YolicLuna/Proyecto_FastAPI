# Models - Documentación

Este directorio contiene los modelos de SQLAlchemy que definen la estructura de las tablas en la base de datos. Cada modelo representa una entidad del sistema y sus relaciones con otras entidades.

## Estructura de Archivos

### `categoria.py`
Define la tabla `categorias`, que almacena las categorías disponibles para clasificar los productos del sistema. Cada categoría tiene un nombre único y mantiene una relación de uno a muchos con la tabla de productos.

**Campos:** `id`, `nombre`
**Relaciones:** Una categoría puede tener muchos productos (`Producto`).

---

### `producto.py`
Define la tabla `productos`, que almacena el catálogo de productos disponibles en la tienda. Incluye información de precio, disponibilidad y cantidad en inventario. Cada producto pertenece a una categoría.

**Campos:** `id`, `nombre`, `precio`, `en_stock`, `stock`, `categoria_id`
**Relaciones:** Muchos productos pertenecen a una categoría (`Categoria`).

---

### `usuario.py`
Define la tabla `usuarios`, que almacena la información de autenticación y autorización de los usuarios del sistema. Las contraseñas nunca se almacenan en texto plano. Cada usuario puede tener un carrito de compras asociado.

**Campos:** `id`, `nombre`, `email`, `hashed_password`, `es_admin`
**Relaciones:** Un usuario tiene un carrito (`Carrito`).

---

### `pedidos.py`
Contiene cuatro modelos relacionados con el flujo de compra del sistema:

**`Carrito`** — Define la tabla `carritos`. Representa el carrito de compras activo de un usuario. Cada usuario puede tener un solo carrito, y este puede contener múltiples productos.
Campos: `id`, `usuarios_id`
Relaciones: Pertenece a un `Usuario`, contiene muchos `ItemCarrito`.

**`ItemCarrito`** — Define la tabla `item_carrito`. Representa cada producto agregado al carrito, incluyendo la cantidad seleccionada.
Campos: `id`, `carrito_id`, `producto_id`, `cantidad`
Relaciones: Pertenece a un `Carrito`, referencia a un `Producto`.

**`Pedido`** — Define la tabla `pedidos`. Representa un pedido confirmado por un usuario, con su fecha de creación y total calculado.
Campos: `id`, `usuario_id`, `fecha`, `total`
Relaciones: Pertenece a un `Usuario`, contiene muchos `DetallePedido`.

**`DetallePedido`** — Define la tabla `detalles_pedidos`. Representa cada línea de un pedido confirmado, con la cantidad y subtotal por producto.
Campos: `id`, `pedido_id`, `producto_id`, `cantidad`, `subtotal`
Relaciones: Pertenece a un `Pedido`, referencia a un `Producto`.

---

## Patrón de Herencia

Todos los modelos heredan de `Base`, la clase base declarativa de SQLAlchemy importada desde `app.db.database`. Esto permite que SQLAlchemy registre automáticamente los modelos y gestione la creación de tablas.

---

## Consideraciones de Seguridad

Las contraseñas de los usuarios siempre se almacenan hasheadas en el campo `hashed_password` y nunca se exponen en las respuestas de la API. El campo `es_admin` controla el acceso a operaciones administrativas del sistema.
