# ==============================
# Importaciones
# ==============================
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
import secrets


# ==============================
# Instancia del servidor
# ==============================
app = FastAPI(
    title='MI primer API',
    description='Ivan Isay Guerra',
    version='1.0.0'
)


# ==============================
# Seguridad HTTP Basic
# ==============================
security = HTTPBasic()

def verificar_Peticion(credentials: HTTPBasicCredentials = Depends(security)):
    username_correcto = secrets.compare_digest(credentials.username, "admin")
    password_correcto = secrets.compare_digest(credentials.password, "1234")

    if not (username_correcto and password_correcto):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


# ==============================
# Base de datos ficticia
# ==============================
usuarios = [
    {"id": 1, "nombre": "Juan", "edad": 21},
    {"id": 2, "nombre": "Israel", "edad": 21},
    {"id": 3, "nombre": "Sofi", "edad": 21},
]


# ==============================
# Modelo Pydantic
# ==============================
class UsuarioBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador Usuario")
    nombre: str = Field(..., min_length=3, max_length=50)
    edad: int = Field(..., ge=0, le=120)


# ==============================
# CRUD USUARIOS
# ==============================

@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def leer_usuarios():
    return {
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }


@app.post("/v1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: UsuarioBase):

    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )

    usuarios.append(usuario)

    return {
        "mensaje": "Usuario Agregado",
        "usuario": usuario
    }


# ==============================
# ENDPOINTS PROTEGIDOS
# ==============================

@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"], status_code=status.HTTP_200_OK)
async def actualizar_usuario(
    id: int,
    usuario_actualizado: UsuarioBase,
    username: str = Depends(verificar_Peticion)
):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:

            usuarios[index] = usuario_actualizado.dict()

            return {
                "message": f"Usuario actualizado completamente por {username}",
                "data": usuario_actualizado
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


@app.patch("/v1/usuarios/{id}", tags=["CRUD HTTP"], status_code=status.HTTP_200_OK)
async def actualizar_parcial(
    id: int,
    datos: dict,
    username: str = Depends(verificar_Peticion)
):
    for usr in usuarios:
        if usr["id"] == id:

            usr.update(datos)

            return {
                "message": f"Usuario actualizado parcialmente por {username}",
                "data": usr
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


@app.delete("/v1/usuarios/{id}", tags=["CRUD HTTP"], status_code=status.HTTP_200_OK)
async def eliminar_usuario(
    id: int,
    username: str = Depends(verificar_Peticion)
):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:

            usuarios.pop(index)

            return {
                "message": f"Usuario eliminado correctamente por {username}"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


# ==============================
# Otros Endpoints
# ==============================

@app.get("/", tags=['Inicio'])
async def bienvenida():
    return {"mensaje": "¡Bienvenido a mi API!"}


@app.get("/HolaMundo", tags=['Bienvenida Asincrona'])
async def hola():
    await asyncio.sleep(3)
    return {
        "mensaje": "¡Hola Mundo FastAPI!",
        "estatus": "200"
    }


@app.get("/v1/parametroOb/{id}", tags=['Parametro Obligatorio'])
async def consultaUno(id: int):
    return {"Se encontro usuario": id}


@app.get("/v1/parametroOp/", tags=['Parametro Opcional'])
async def consultaTodos(id: Optional[int] = None):
    if id is not None:
        for usuariok in usuarios:
            if usuariok["id"] == id:
                return {"mensaje": "usuario encontrado", "usuario": usuariok}
        return {"mensaje": "usuario no encontrado", "usuario": id}
    else:
        return {"mensaje": "No se proporciono id"}