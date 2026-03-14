from fastapi import FastAPI
from app.routers import usuarios, misc
from app.data.db import engine
from app.models import usuarioDB

usuarioDB.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MI primer API",
    description="Ivan Isay Guerra",
    version="1.0.0"
)

app.include_router(usuarios.router)
app.include_router(misc.router)