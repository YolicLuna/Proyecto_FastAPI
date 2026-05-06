# FastAPI E-commerce API

API RESTful completa para la gestión de un E-commerce, desarrollada con FastAPI y SQLAlchemy. Incluye autenticación con JWT, administración de productos y categorías, carrito de compras y gestión de pedidos.

---

## Descripción General

Este proyecto implementa el backend de una tienda en línea. Permite a los usuarios registrarse, autenticarse, agregar productos a su carrito y confirmar pedidos. Los administradores pueden gestionar el catálogo de productos y categorías.

---

## Requisitos

- Python 3.10+
- MySQL

---

## Inicio Rápido

**1. Instalar dependencias:**
```bash
pip install -r requirements.txt
```

**2. Configurar variables de entorno** creando un archivo `.env` en la raíz:
```
SECRET_KEY=tu_clave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost:3306/api
```

**3. Inicializar la base de datos:**
```bash
mysql -u usuario -p < Data_base.sql
```

**4. Ejecutar la aplicación:**
```bash
python -m uvicorn main:app --reload
```

**5. Acceder a la documentación interactiva:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Estructura del Proyecto

```
app/
├── main.py              # Punto de entrada de la aplicación
├── requirements.txt     # Dependencias del proyecto
├── Data_base.sql        # Script de inicialización de la BD
├── alembic.ini          # Configuración de Alembic
├── api/                 # Rutas y endpoints de la API (v1)
├── core/                # Configuración y seguridad
├── crud/                # Operaciones de base de datos
├── db/                  # Configuración de la conexión a BD
├── deps/                # Dependencias inyectables de FastAPI
├── models/              # Modelos SQLAlchemy
├── schemas/             # Esquemas Pydantic
└── tests/               # Pruebas automatizadas
```

---

## Endpoints Disponibles

### Autenticación — `/api/v1/auth`
| Método | Ruta | Descripción | Autenticación |
|--------|------|-------------|---------------|
| POST | /usuarios | Registrar nuevo usuario | No |
| POST | /login | Iniciar sesión y obtener token JWT | No |
| GET | /usuarios/me | Obtener perfil del usuario autenticado | Sí |
| GET | /admin/ping | Endpoint de prueba para administradores | Admin |

### Productos — `/api/v1/producto`
| Método | Ruta | Descripción | Autenticación |
|--------|------|-------------|---------------|
| GET | / | Listar todos los productos | No |
| POST | /productos | Crear nuevo producto | Admin |
| PUT | /productos/{id} | Actualizar producto | Admin |
| DELETE | /productos/{id} | Eliminar producto | Admin |

### Categorías — `/api/v1/categorias`
| Método | Ruta | Descripción | Autenticación |
|--------|------|-------------|---------------|
| GET | /categorias | Listar todas las categorías | No |
| POST | /categorias | Crear nueva categoría | Sí |

### Carrito — `/api/v1/carrito`
| Método | Ruta | Descripción | Autenticación |
|--------|------|-------------|---------------|
| GET | / | Ver contenido del carrito | Sí |
| POST | /agregar/{producto_id} | Agregar producto al carrito | Sí |
| DELETE | /eliminar/{item_id} | Eliminar producto del carrito | Sí |

### Pedidos — `/api/v1/pedido`
| Método | Ruta | Descripción | Autenticación |
|--------|------|-------------|---------------|
| POST | /confirmar | Confirmar pedido desde el carrito | Sí |

---

## Dependencias Principales

| Dependencia | Propósito |
|-------------|-----------|
| fastapi | Framework web para construir la API |
| uvicorn | Servidor ASGI para ejecutar la aplicación |
| SQLAlchemy | ORM para interacción con la base de datos |
| PyMySQL | Driver MySQL |
| passlib[bcrypt] | Hash seguro de contraseñas |
| python-jose[cryptography] | Generación y validación de tokens JWT |
| email-validator | Validación de correos electrónicos |
| python-multipart | Soporte para formularios en FastAPI |
| bcrypt==4.0.1 | Backend de hashing criptográfico para passlib |
| python-dotenv | Carga de variables de entorno desde `.env` |
| alembic | Migraciones de base de datos |
| pytest | Framework para pruebas automatizadas |
| httpx | Cliente HTTP requerido por TestClient de FastAPI |

---

## Seguridad

La autenticación se implementa con tokens JWT. Las contraseñas se almacenan siempre hasheadas con bcrypt. Los endpoints sensibles requieren un token válido en el header `Authorization: Bearer <token>`, y los endpoints administrativos verifican adicionalmente el campo `es_admin` del usuario.

---

## Pruebas

```bash
cd app
pytest -v
```

Las pruebas cubren autenticación, validación de datos y operaciones CRUD de productos.

---

## Autor

José Yolic — Equipo Backend
[GitHub](https://github.com/YolicLuna/Proyecto_FastAPI) · yolicdev@gmail.com
