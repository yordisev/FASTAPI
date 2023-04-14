from fastapi import FastAPI
from routes.login import loginsistema
from routes.user import user
from routes.archivos import archivos

app = FastAPI()

app.include_router(loginsistema)
app.include_router(user)
app.include_router(archivos)