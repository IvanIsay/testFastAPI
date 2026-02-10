from fastapi import FastAPI
from fastapi import status,HTTPException

app= FastAPI()

#BD ficticia
usuarios=[
    {"id": 1,"nombre":"ivan", "edad":37},
    {"id": 2,"nombre":"isay", "edad":15},
    {"id": 3,"nombre":"petra", "edad":18},
    {"id": 4,"nombre":"ana", "edad":37}
]

#Endpoint home
@app.get('/')
def home():
    return {'hello':'world FastAPI'}

#CRUD para usuarios

@app.get("/v1/usuarios/", tags=["Usuarios CRUD"])
async def leer_usuarios():
    return {
        "status": "ok",
        "total": len(usuarios),
        "data": usuarios
    }
    
@app.post("/v1/usuarios/", tags=["Usuarios CRUD"], status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: dict):

    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El id  ya existe"
            )

    usuarios.append(usuario)

    return {
        "message": "Usuario creado correctamente",
        "data": usuario
    }