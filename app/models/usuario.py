from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from app.db.database import Base

# Clase para la tabla de usuarios en la base de datos.
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    es_admin = Column(Boolean, default=False)
