from pydantic import BaseModel

# Clases para la categoria
class CategoriaBase(BaseModel):
    nombre: str

# Clase de respuesta para la categoria, que incluye el ID generado por la base de datos.
class CategoriaCreate(CategoriaBase):
    pass

# Clase de respuesta para la categoria, que incluye el ID generado por la base de datos.
class CategoriaResponse(CategoriaBase):
    id: int
    class Config:
        from_attributes = True
