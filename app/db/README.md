# DB - Documentación

Este directorio contiene la configuración y gestión de la conexión a la base de datos. Incluye la inicialización del motor de SQLAlchemy y la creación de tablas.

## Estructura de Archivos

### `database.py`
**Propósito:** Configuración principal de la base de datos.

Este archivo establece la conexión a la base de datos y crea los componentes esenciales de SQLAlchemy.

**Componentes principales:**

#### `engine`
- Motor de SQLAlchemy que gestiona la conexión a la base de datos.
- Se crea utilizando la `DATABASE_URL` de la configuración (`setting.DATABASE_URL`).
- Responsable de ejecutar todas las operaciones SQL.

```python
engine = create_engine(setting.DATABASE_URL)
```

#### `session_local`
- Factory de sesiones para crear instancias de sesión.
- Configurado con:
  - `autocommit=False` - Los cambios no se confirman automáticamente.
  - `autoflush=False` - Los cambios no se envían automáticamente.
  - `bind=engine` - Vinculado al motor de la base de datos.
- Se utiliza para crear sesiones en cada solicitud HTTP.

```python
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

#### `Base`
- Clase base declarativa para definir modelos de SQLAlchemy.
- Todos los modelos (Usuario, Producto, Categoría) heredan de `Base`.
- Mantiene un registro de todos los modelos definidos para crear las tablas.

```python
Base = declarative_base()
```

**Importaciones en otros módulos:**
```python
from app.db.database import engine, Base, session_local
```

---

### `init_db.py`
**Propósito:** Inicialización de la base de datos y creación de tablas.

Este script se utiliza para crear todas las tablas en la base de datos basándose en los modelos definidos.

**Función principal:**
- Utiliza `Base.metadata.create_all()` para crear todas las tablas definidas en los modelos.
- Se ejecuta una sola vez durante la configuración inicial del proyecto.
- Imprime un mensaje de confirmación cuando las tablas se crean correctamente.

```python
Base.metadata.create_all(bind=engine)
print('Tablas creadas correctamente.')
```

**¿Cuándo ejecutar?**
- Al iniciar el proyecto por primera vez.
- Después de agregar nuevos modelos que requieren nuevas tablas.
- Durante el desarrollo cuando se necesitan reinicializar las tablas.

**Ejecución manual:**
```bash
python app/db/init_db.py
```

---

## Flujo de Inicialización

1. **Import `database.py`**
   - Se crea el `engine` conectado a la base de datos.
   - Se crea la factory `session_local` para crear sesiones.
   - Se define la clase base `Base` para los modelos.

2. **Definición de Modelos**
   - Los modelos heredan de `Base` (ej: `class Usuario(Base)`).
   - SQLAlchemy registra automáticamente los modelos.

3. **Ejecución de `init_db.py`**
   - Lee todos los modelos registrados en `Base.metadata`.
   - Crea las tablas correspondientes en la base de datos.

---

## Uso en la Aplicación

### En los endpoints (para obtener sesión):
```python
from app.db.database import session_local
from sqlalchemy.orm import Session

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
