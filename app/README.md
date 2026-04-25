# FastAPI Application.

## Descripción General.

Esta es la carpeta principal de la aplicación FastAPI que contiene toda la estructura y configuración del proyecto backend.

---

## 📄 Archivos Principales

### **main.py**

Es el punto de entrada de la aplicación FastAPI. Encargado de:

- Crear la instancia principal de la aplicación FastAPI.
- Incluir el router de la API con el prefijo `/api/v1` para organizar todas las rutas bajo esa versión.

**Para ejecutar la aplicación:**
```bash
python -m uvicorn main:app --reload
```

**Parámetros útiles:**
- `--reload`: Reinicia el servidor automáticamente al detectar cambios (desarrollo).
- `--port 8000`: Especifica el puerto (por defecto es 8000).

---

### **requirements.txt**

Archivo que contiene todas las dependencias del proyecto:

| Dependencia | Propósito |
|---|---|
| **fastapi** | Framework web moderno para construir APIs REST |
| **uvicorn** | Servidor ASGI para ejecutar la aplicación FastAPI |
| **SQLAlchemy** | ORM para interacción con la base de datos |
| **PyMySQL** | Driver MySQL para conexión a la BD |
| **passlib[bcrypt]** | Librería para hash seguro de contraseñas |
| **python-jose[cryptography]** | Implementación de JSON Web Tokens (JWT) para autenticación |
| **email-validator** | Validación de direcciones de correo electrónico |
| **python-multipart** | Soporte para formularios multipart en FastAPI |
| **bcrypt** | Hashing criptográfico para contraseñas |
| **python-dotenv** | Carga de variables de entorno desde archivos `.env` |
| **alembic** | Herramienta para migraciones de base de datos |

**Para instalar las dependencias:**
```bash
pip install -r requirements.txt
```

---

### **Data_base.sql**

Archivo SQL que contiene los comandos iniciales para configurar la base de datos:

```sql
CREATE DATABASE IF NOT EXISTS api;  -- Crea la BD si no existe
USE api;                             -- Selecciona la BD a utilizar
SHOW DATABASES;                      -- Lista todas las BD
SHOW TABLES;                         -- Lista las tablas de la BD actual
```

**Para ejecutar este archivo en MySQL:**
```bash
mysql -u usuario -p < Data_base.sql
```

---

### **alembic/**

**Propósito:**
Alembic es una herramienta de migraciones de base de datos que permite versionear los cambios en la estructura de la BD de forma ordenada y controlada.

**Uso en el proyecto:**

- **Crear migraciones**: Cuando se modifican los modelos SQLAlchemy, Alembic genera scripts de migración que registran esos cambios.
- **Aplicar cambios**: Las migraciones se pueden aplicar incrementalmente a la BD.
- **Historial de cambios**: Mantiene un historial de todas las versiones de la BD.

**Archivos importantes:**
- `alembic.ini`: Configuración de Alembic.
- `env.py`: Script de configuración del entorno de migraciones.
- `versions/`: Carpeta que almacena los scripts de migración versionados.

**Comandos útiles:**
```bash
alembic revision --autogenerate -m "Descripción del cambio"  # Crear nueva migración
alembic upgrade head                                           # Aplicar todas las migraciones
alembic downgrade -1                                           # Revertir última migración
```

---

## 📁 Estructura del Proyecto

```
app/
├── main.py                 # Punto de entrada de la aplicación.
├── requirements.txt        # Dependencias del proyecto.
├── Data_base.sql          # Script de inicialización de BD.
├── alembic.ini            # Configuración de Alembic.
├── api/                   # Rutas y endpoints de la API.
├── core/                  # Configuración y seguridad.
├── crud/                  # Operaciones CRUD para modelos.
├── db/                    # Configuración de base de datos.
├── deps/                  # Dependencias compartidas.
├── models/                # Modelos SQLAlchemy.
├── schemas/               # Esquemas Pydantic (validación).
└── alembic/              # Migraciones de base de datos.
```

---

## 🚀 Inicio Rápido

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar la base de datos:**
   ```bash
   mysql -u usuario -p < Data_base.sql
   ```

3. **Ejecutar la aplicación:**
   ```bash
   python -m uvicorn main:app --reload
   ```

4. **Acceder a la documentación interactiva:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

---

