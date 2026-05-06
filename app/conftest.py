import sys
import os

# Se agrega el directorio raíz del proyecto al sys.path para poder importar el módulo main y acceder a la aplicación FastAPI. 
# Esto es necesario para que las pruebas puedan interactuar con la aplicación y realizar solicitudes HTTP a los endpoints.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))