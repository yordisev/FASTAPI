from typing import Optional
from pydantic import BaseModel

class Usuarios(BaseModel):
    # id_usuario: Optional[int]
    tipo_documento:str
    numero_documento:int
    nombres:str
    apellidos:str
    departamento:int
    municipio:int
    usuario:str
    password:str