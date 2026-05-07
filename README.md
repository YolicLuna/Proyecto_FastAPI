# FastAPI E-commerce API

API RESTful completa para la gestión de un E-commerce, desarrollada con FastAPI y SQLAlchemy. Incluye autenticación con JWT, administración de productos y categorías, carrito de compras y gestión de pedidos.

---

## Descripción General

Este proyecto consiste en una API RESTful desarrollada con FastAPI y SQLAlchemy, orientada a la gestión completa de un sistema de comercio electrónico. La aplicación permite a los usuarios registrarse, autenticarse mediante tokens JWT, explorar un catálogo de productos, administrar su 
carrito de compras y confirmar pedidos. Los administradores cuentan con privilegios adicionales para gestionar productos y categorías del sistema.
### Tecnologías Utilizadas
El proyecto está construido sobre FastAPI como framework principal para la definición de endpoints y la gestión de solicitudes HTTP. SQLAlchemy actúa como ORM para el manejo de la base de datos relacional MySQL, a la que se conecta a través del driver PyMySQL. La validación y serialización de datos se realiza con Pydantic. La autenticación se implementa con JSON Web Tokens mediante la librería python-jose, y el hashing de contraseñas se gestiona con passlib y bcrypt. La configuración del entorno se administra con python-dotenv, y las migraciones de base de datos se manejan con Alembic. Las pruebas automatizadas utilizan pytest junto con httpx y el TestClient de FastAPI.

### Arquitectura del Proyecto
El proyecto sigue una arquitectura de capas claramente separadas. La capa de modelos define la estructura de las tablas en la base de datos mediante clases SQLAlchemy. La capa de esquemas contiene las clases Pydantic encargadas de validar los datos de entrada y serializar las respuestas. La capa CRUD centraliza todas las operaciones de acceso a datos, separando la lógica de negocio de los endpoints. La capa de dependencias provee funciones reutilizables para la inyección de sesiones de base de datos y la validación de autenticación. Finalmente, la capa de API organiza los endpoints en módulos independientes agrupados bajo el prefijo /api/v1.

### Modelos de la Base de Datos
El sistema cuenta con cinco entidades principales. La entidad Categoría almacena las categorías del catálogo, cada una con un nombre único. La entidad Producto representa los artículos disponibles en la tienda, con campos de nombre, precio, disponibilidad en stock, cantidad en inventario y referencia a su categoría. La entidad Usuario guarda la información de autenticación de los usuarios, incluyendo nombre, correo electrónico, contraseña hasheada y un indicador de rol administrativo. La entidad Carrito representa el carrito de compras activo de cada usuario, que puede contener múltiples ítems a través de la entidad ItemCarrito. Para los pedidos confirmados, existen las entidades Pedido y DetallePedido, que 
registran el total de la compra, la fecha y el detalle de cada producto adquirido.

### Seguridad y Autenticación
La seguridad del sistema se basa en dos pilares. El primero es el hashing de contraseñas con bcrypt, que garantiza que ninguna contraseña se almacene en texto plano en la base de datos. El segundo es la autenticación mediante tokens JWT, que se generan al momento del inicio de sesión e incluyen el correo del usuario, su rol y una fecha de expiración configurable. Los endpoints protegidos validan el token en cada solicitud, y los endpoints administrativos adicionalmente verifican que el usuario tenga el atributo es_admin activado. Las contraseñas y el token nunca se exponen en las respuestas de la API.

### Flujo de Compra
El flujo de compra inicia cuando un usuario autenticado agrega productos a su carrito mediante el endpoint correspondiente. Si el producto ya existe en el carrito, la cantidad se incrementa automáticamente. Una vez listo, el usuario puede confirmar el pedido, momento en el que el sistema valida que el carrito no este vacío, verifica la disponibilidad de stock de cada producto, calcula el total del pedido, genera los registros de detalle, descuenta el inventario y limpia el carrito. Si un producto no tiene stock suficiente o no está disponible, ese ítem se omite del pedido.

### Pruebas Automatizadas
El proyecto incluye pruebas automatizadas escritas con pytest y el TestClient de FastAPI. Las pruebas cubren la validación de credenciales incorrectas en el login, la disponibilidad de la documentación automática de Swagger, la creación exitosa de productos con datos válidos, la respuesta de error ante datos incompletos, y el listado del catálogo de productos. Las pruebas no requieren levantar el servidor manualmente, ya que el TestClient simula las solicitudes HTTP directamente sobre la aplicación.


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
