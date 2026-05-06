-# Tests - Documentación

Este directorio contiene las pruebas automatizadas de la API, escritas con `pytest` y el `TestClient` de FastAPI. Las pruebas verifican el comportamiento de los endpoints sin necesidad de levantar el servidor manualmente.

## Configuración General

Cada archivo de prueba agrega el directorio raíz del proyecto al `sys.path` para poder importar la aplicación FastAPI desde `main.py`. Se utiliza `TestClient` para simular solicitudes HTTP a los endpoints durante las pruebas.

---

## Estructura de Archivos

### `test_auth.py`
Contiene pruebas relacionadas con la autenticación y el acceso general a la API.

`test_login_invalid` verifica que un intento de inicio de sesión con credenciales incorrectas retorne un código de estado 401, confirmando que el sistema rechaza accesos no autorizados.

`test_ping_docs` verifica que la documentación automática de Swagger esté disponible y retorne un código de estado 200.

---

### `test_productos.py`
Contiene pruebas relacionadas con el CRUD de productos. Utiliza un token JWT de administrador para acceder a los endpoints protegidos.

`test_crear_producto_exitoso` envía una solicitud de creación de producto con todos los campos válidos y verifica que la respuesta sea 200 y que los datos del producto creado coincidan con los enviados.

`test_crear_producto_faltante_nombre` envía una solicitud de creación de producto sin el campo `nombre` y verifica que la respuesta sea 422, confirmando que la validación de Pydantic funciona correctamente.

`test_listar_productos` verifica que el endpoint de listado de productos retorne un código 200 y que la respuesta sea una lista.

---

## Resumen de Pruebas

| Archivo | Test | Endpoint | Código esperado |
|---------|------|----------|----------------|
| test_auth.py | test_login_invalid | POST /api/v1/auth/login | 401 |
| test_auth.py | test_ping_docs | GET /docs | 200 |
| test_productos.py | test_crear_producto_exitoso | POST /api/v1/producto/productos | 200 |
| test_productos.py | test_crear_producto_faltante_nombre | POST /api/v1/producto/productos | 422 |
| test_productos.py | test_listar_productos | GET /api/v1/producto/ | 200 |

---

## Nota sobre el Token

Las pruebas de productos utilizan un token JWT hardcodeado obtenido mediante Insomnia con un usuario administrador. Este token tiene fecha de expiración, por lo que deberá actualizarse cuando expire para que las pruebas protegidas sigan funcionando.
