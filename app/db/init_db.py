from app.db.database import engine, Base

# Creamos las tablas en la base de datos
Base.metadata.create_all(bind=engine)
print('Tablas creadas correctamente.')
