from fastapi import FastAPI
from dotenv import load_dotenv
from routes.login import loginsistema
from routes.user import user
from routes.archivos import archivos

app = FastAPI()

app.include_router(loginsistema)
app.include_router(user)
app.include_router(archivos)
load_dotenv()