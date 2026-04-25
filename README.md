# 🚀 Proyecto FastAPI - API de Gestión de Productos.

## 📋 Descripción del Proyecto.

Esta es una **API REST** moderna construida con **FastAPI** que permite gestionar un catálogo de productos y usuarios de manera segura y eficiente.

### ¿Qué hace?

- ✅ **Gestión de Productos:** Crear, consultar, actualizar y eliminar productos del catálogo.
- ✅ **Organización por Categorías:** Clasificar productos en diferentes categorías.
- ✅ **Autenticación Segura:** Sistema de login con tokens JWT para proteger los endpoints.
- ✅ **Gestión de Usuarios:** Administración de usuarios con roles y permisos.
- ✅ **Base de Datos:** Almacenamiento persistente en MySQL.

---

## 🏗️ Estructura del Proyecto.

El proyecto está organizado de forma modular para facilitar el mantenimiento y escalabilidad:

| Carpeta | Función |
|---------|---------|
| **`app/`** | Núcleo de la aplicación con toda la lógica |
| **`api/`** | Definición de los endpoints y rutas de la API |
| **`models/`** | Estructura de datos en la base de datos |
| **`schemas/`** | Validación y transformación de datos de entrada/salida |
| **`crud/`** | Operaciones de base de datos (crear, leer, actualizar, eliminar) |
| **`core/`** | Configuración general y funciones de seguridad |
| **`db/`** | Conexión y gestión de la base de datos |
| **`deps/`** | Herramientas reutilizables para los endpoints |
| **`alembic/`** | Historial de cambios en la estructura de la base de datos |

---

## 🎯 Características Principales.

### 🔐 Seguridad.
- Autenticación basada en JWT (JSON Web Tokens).
- Contraseñas cifradas con bcrypt.
- Validación de credenciales en cada solicitud.

### 📊 Datos Estructurados.
- Modelos bien definidos para Productos, Categorías y Usuarios.
- Validación automática de datos de entrada.
- Documentación clara de cada campo.

### 🔄 Operaciones CRUD Completas.
- Crear nuevos registros.
- Consultar información existente.
- Actualizar datos.
- Eliminar registros.

### 📱 API Moderna.
- Interfaz REST estándar.
- Documentación automática interactiva (Swagger UI).
- Responses consistentes y bien formateadas.

---

## 📖 Para Más Información.

Cada carpeta del proyecto contiene su propio `README.md` con documentación detallada:

- [📚 Documentación de la Aplicación](app/README.md) - Inicio rápido, dependencias y archivos. principales
- [🔌 Documentación de la API](app/api/README.md) - Endpoints y rutas disponibles.
- [🎛️ Documentación del Core](app/core/README.md) - Configuración y seguridad.
- [💾 Documentación de la BD](app/db/README.md) - Conexión y gestión de datos.
- [📦 Documentación de Modelos](app/models/README.md) - Estructura de entidades.
- [✔️ Documentación de Schemas](app/schemas/README.md) - Validación de datos.
- [🗂️ Documentación CRUD](app/crud/README.md) - Operaciones de base de datos.
- [🔗 Documentación de Deps](app/deps/README.md) - Dependencias inyectables.

---

## 🚀 Inicio Rápido.

Para más detalles sobre cómo ejecutar la aplicación, consulta [app/README.md](app/README.md).

```bash
# 1. Instalar dependencias
pip install -r app/requirements.txt

# 2. Configurar base de datos
mysql -u usuario -p < app/Data_base.sql

# 3. Ejecutar la aplicación
cd app
python -m uvicorn main:app --reload
```

**Luego accede a:**
- 📖 Documentación interactiva: http://localhost:8000/docs
- 🎨 Documentación alternativa: http://localhost:8000/redoc

---

## 📌 Notas

Este proyecto utiliza tecnologías modernas de desarrollo backend:
- **FastAPI** para crear APIs rápidas y seguras.
- **SQLAlchemy** para interactuar con la base de datos.
- **MySQL** como gestor de datos.
- **JWT** para autenticación segura.

Toda la información técnica detallada está en los README de cada carpeta.
