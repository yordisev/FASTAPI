from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from werkzeug.security import check_password_hash
from config.conexion import create_db_connection
from schema.login import Login
from config.token import write_token

loginsistema = APIRouter()



@loginsistema.post("/login", description="Acceso al sistema")
def Acceso_al_sistema(payload: Login):
    _json = jsonable_encoder(payload)
    _username = _json['usuario']
    _password = _json['password']
    # validate the received values
    if _username and _password:
        connection = create_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT usuario,password FROM db_usuarios WHERE usuario=%s"
        cursor.execute(query, (_username,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        username = result['usuario']
        password = result['password']
        if result:
            if check_password_hash(password, _password):
                cursor.close()
                token_creado = write_token(jsonable_encoder(result))
                return JSONResponse(content={'message' : 'You are logged in successfully','token':token_creado},status_code=201)
            else:
                resp = JSONResponse(content={'message' : 'Bad Request - invalid password'},status_code=404)
                return resp
        else:
            resp = JSONResponse(content={'message' : 'Bad Request - invalid credendtials'},status_code=404)
        return resp