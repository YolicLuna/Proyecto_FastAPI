from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from core.config import setting

# Crear el motor de la base de datos, la sesión local y la base declarativa para SQLAlchemy, 
# utilizando la URL de la base de datos especificada en la configuración.
engine = create_engine(setting.DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
