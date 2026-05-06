# Schemas - Documentación

Este directorio contiene los esquemas Pydantic que definen la validación y serialización de datos en la API. Los schemas actúan como intermediarios entre las solicitudes HTTP (JSON) y los modelos de base de datos (SQLAlchemy).

## Propósito de los Schemas

Los schemas se encargan de validar automáticamente los datos de entrada, serializar modelos ORM a JSON para las respuestas, generar documentación automática en Swagger, y controlar qué campos se exponen en cada respuesta de la API.

---

## Estructura de Archivos

### `categoria.py`
Define los esquemas para las categorías de productos. Contiene tres clases con una estructura jerárquica.

`CategoriaBase` es la clase base que define el campo `nombre`. `CategoriaCreate` hereda de ella y se usa para validar los datos al crear una categoría. `CategoriaResponse` también hereda de la base y agrega el campo `id` generado por la base de datos; incluye la configuración `from_attributes = True` para trabajar con objetos ORM.

---

### `producto.py`
Define los esquemas para los productos del catálogo. Contiene dos clases.

`ProductoCreate` define los campos requeridos para crear un producto: `nombre`, `precio`, `en_stock` y `categoria_id`. `ProductoResponse` hereda de `ProductoCreate` y agrega el campo `id`; incluye la configuración `from_attributes = True` para serializar objetos ORM automáticamente.

---

### `usuario.py`
Define los esquemas para la gestión de usuarios y autenticación. Contiene cuatro clases.

`UsuarioBase` es la clase base con los campos `nombre` y `email`, donde el email es validado automáticamente por Pydantic mediante `EmailStr`.

`UsuarioCreate` hereda de `UsuarioBase` y agrega `password` (contraseña en texto plano, que será hasheada en el CRUD) y `es_admin` (booleano con valor por defecto `False`).

`UsuarioResponse` hereda de `UsuarioBase` y agrega `id` y `es_admin`. No incluye la contraseña por seguridad. Incluye la configuración `from_attributes = True`.

`Token` es una clase independiente que representa la respuesta del login. Contiene `access_token` con el JWT generado y `token_type` con valor por defecto `bearer`.

---

## Patrón de Herencia

Se utilizan clases base (`CategoriaBase`, `UsuarioBase`) para evitar la repetición de campos comunes. Las clases específicas (`Create`, `Response`) heredan de la base y agregan o ajustan campos según su propósito — entrada de datos vs. respuesta de la API.

---

## Configuración `from_attributes = True`

Presente en `CategoriaResponse`, `ProductoResponse` y `UsuarioResponse`. Permite a Pydantic convertir automáticamente objetos ORM de SQLAlchemy a JSON sin necesidad de conversión manual.

---

## Resumen de Schemas

| Schema | Campos | Propósito |
|--------|--------|-----------|
| CategoriaCreate | nombre | Crear categoría |
| CategoriaResponse | id, nombre | Respuesta de categoría |
| ProductoCreate | nombre, precio, en_stock, categoria_id | Crear producto |
| ProductoResponse | id, nombre, precio, en_stock, categoria_id | Respuesta de producto |
| UsuarioCreate | nombre, email, password, es_admin | Registrar usuario |
| UsuarioResponse | id, nombre, email, es_admin | Perfil de usuario |
| Token | access_token, token_type | Respuesta de login |
