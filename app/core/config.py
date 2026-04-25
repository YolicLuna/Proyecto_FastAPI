from pydantic_settings import BaseSettings

# Se define una clase de configuración utilizando Pydantic, 
# que permite cargar las variables de entorno desde un archivo .env 
# y acceder a ellas de manera sencilla en toda la aplicación.
class Setting(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

# Se crea una instancia global de la clase de configuración,
# que se puede importar y utilizar en cualquier parte de la aplicación 
# para acceder a las variables de entorno.
setting = Setting()

