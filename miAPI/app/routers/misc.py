from fastapi import APIRouter
import asyncio
from typing import Optional
from app.data.database import usuarios

router = APIRouter(tags=["General"])

@router.get("/")
async def bienvenida():
    return {"mensaje": "¡Bienvenido a mi API!"}

@router.get("/HolaMundo")
async def hola():
    await asyncio.sleep(3)
    return {
        "mensaje": "¡Hola Mundo FastAPI!",
        "estatus": "200"
    }

@router.get("/v1/parametroOb/{id}")
async def consultaUno(id: int):
    return {"Se encontro usuario": id}

@router.get("/v1/parametroOp/")
async def consultaTodos(id: Optional[int] = None):

    if id is not None:
        for usuariok in usuarios:
            if usuariok["id"] == id:
                return {"mensaje": "usuario encontrado", "usuario": usuariok}

        return {"mensaje": "usuario no encontrado", "usuario": id}

    return {"mensaje": "No se proporciono id"}