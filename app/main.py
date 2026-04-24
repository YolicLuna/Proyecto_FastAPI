from fastapi import FastAPI, Depends, HTTPException, status
from api.v1.api import api_router

# Crear la aplicación FastAPI.
app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

# python -m uvicorn main:app --reload (Comando para correr el programa)
