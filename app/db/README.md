# DB - Documentación

Este directorio contiene la configuración y gestión de la conexión a la base de datos. Incluye la inicialización del motor de SQLAlchemy, la creación de sesiones y la configuración de la base declarativa para los modelos ORM.

## Propósito de la Carpeta

La carpeta `db` centraliza toda la configuración relacionada con la base de datos, permitiendo:

- Establecer una conexión centralizada a la base de datos.
- Crear sesiones reutilizables para las operaciones CRUD.
- Definir una clase base común para todos los modelos SQLAlchemy.
- Inicializar y crear todas las tablas de la base de datos de forma automática.
- Facilitar la inyección de dependencias de sesión en los endpoints.

## Estructura de Archivos

### `database.py`
Configura los componentes esenciales de SQLAlchemy para conectarse a la base de datos. Crea el motor (engine) que gestiona todas las conexiones SQL, la factory de sesiones que proporciona instancias de sesión reutilizables, y la clase base declarativa que sirve como padre para todos los modelos ORM de la aplicación. Este archivo es importado por todas partes de la aplicación que requieren acceso a la base de datos.

### `init_db.py`
Script de inicialización que crea todas las tablas en la base de datos basándose en los modelos definidos en la aplicación. Se ejecuta manualmente una sola vez al configurar el proyecto por primera vez, después de agregar nuevos modelos, o cuando se necesita reinicializar la estructura de la base de datos. Genera las tablas y confirma la creación exitosa.

## Integración con la Aplicación

- **Conexión centralizada:** El `engine` y `session_local` se importan desde `database.py` en toda la aplicación.
- **Inyección de dependencias:** Las sesiones se inyectan en los endpoints de FastAPI a través de `Depends()`.
- **Modelos ORM:** Todos los modelos (Usuario, Producto, Categoría, Pedido, Carrito) heredan de la clase `Base`.
- **Type hints:** La sesión se tipifica como `Session` en los parámetros de funciones y endpoints.

## Flujo de Inicialización

1. **Importación de `database.py`:** Se establece la conexión y se crea la factory de sesiones.
2. **Definición de modelos:** Los modelos de la aplicación heredan de `Base` y se registran automáticamente.
3. **Ejecución de `init_db.py`:** Se crean todas las tablas correspondientes en la base de datos.
4. **Uso en endpoints:** Los endpoints utilizan sesiones inyectadas para realizar operaciones CRUD.

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
```

### En los CRUD (para operaciones):
```python
from sqlalchemy.orm import Session
from app.db.database import Base

def obtener_usuarios(db: Session):
    return db.query(Usuario).all()
```

---

## Variables de Configuración Requeridas

Estas variables deben estar en el archivo `.env`:
- `DATABASE_URL` - URL de conexión a la base de datos.
  - Ejemplo MySQL: `mysql+pymysql://usuario:contraseña@localhost:3306/nombre_bd`.
  - Ejemplo PostgreSQL: `postgresql://usuario:contraseña@localhost:5432/nombre_bd`.
