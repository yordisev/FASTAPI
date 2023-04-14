from pydantic import BaseModel

class Login(BaseModel):
    usuario:str
    password:int