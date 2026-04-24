from pydantic import BaseModel

# Clase base para el producto, con los campos comunes.
class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    en_stock: bool
    categoria_id: int

# Clase de respuesta para el producto, que incluye el ID generado por la base de datos.
class ProductoResponse(ProductoCreate):
    id: int
    class Config:
        from_attributes = True