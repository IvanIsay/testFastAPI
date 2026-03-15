from fastapi import FastAPI
from app.routers import usuarios, misc
from app.data.db import engine
from app.data import usuarioDB

#pertenece al funcionamiento del ORM de SQLAlchemy y sirve para 
#crear automáticamente las tablas en la base de datos si aún no existen.
usuarioDB.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="MI primer API",
    description="Ivan Isay Guerra",
    version="1.0.0"
)

app.include_router(usuarios.router)
app.include_router(misc.router)