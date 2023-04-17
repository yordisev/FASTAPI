from jwt import encode, decode
# from jwt import exceptions
from config.conexion import create_db_connection
from datetime import datetime, timedelta
from os import getenv
# from fastapi.responses import JSONResponse

def expire_date(days: int):
    date = datetime.now()
    new_date = date + timedelta(days)
    return new_date

def write_token(data: dict):
    token = encode(payload={**data, "exp": expire_date(2) }, key=getenv("SECRET"), algorithm="HS256")
    return token


# def validate_token(token, output=False):
#     try:
#         if token:
#             validartoken = token.split(" ")[1]
#             return decode(validartoken, key=getenv("SECRET"), algorithms=["HS256"])
#         decode(token, key=getenv("SECRET"), algorithms=["HS256"])
#     except exceptions.DecodeError:
#         return JSONResponse(content={"message": "Invalid Token"}, status_code=401)
#     except exceptions.ExpiredSignatureError:
#         return JSONResponse(content={"message": "Token Expired"}, status_code=401)
    

    # return write_token(user.dict())
    # token = Authorization.split(" ")[1]
    # return validate_token(token, output=True)
def validate_token(token):
    try:
        validartoken = token.split(" ")[1]
        tokenlisto = decode(validartoken, key=getenv("SECRET"), algorithms=["HS256"])
        if "usuario" in tokenlisto:
            connection = create_db_connection()
            cursor = connection.cursor(dictionary=True)
            query = "SELECT id_usuario FROM db_usuarios WHERE usuario=%s"
            cursor.execute(query, (tokenlisto['usuario'],))
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            if result:
                print("Token Valido")
                return True
            else:
                print("El token es inválido: no se encontró el usuario en la base de datos")
                return False
        else:
            print("El token es inválido: no se encontró el usuario en el token")
            return False
    except:
        print("El token es inválido: ocurrió un error al validar el token")
        return False