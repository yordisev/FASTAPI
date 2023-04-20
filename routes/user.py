from fastapi import APIRouter, Request, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from werkzeug.security import generate_password_hash
from config.validar_key import Validar_Token
from config.token import validate_token
from config.conexion import create_db_connection
from schema.usuarios import Usuarios
import socket
user = APIRouter()

@user.get("/hostname/{ip_cliente}")
def read_client_pc_name(ip_cliente: str):
    try:
        pc_name = socket.gethostbyaddr(ip_cliente)[0]
        
    except socket.herror:
        pc_name = "Nombre del PC no encontrado"
    return {"nombre_pc": pc_name}

@user.get("/puerto/{ip_cliente}&{puerto}")
def read_client_puerto(ip_cliente: str,puerto: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    resultado = sock.connect_ex((ip_cliente, puerto))
    sock.close()
    if resultado == 0:
        return {"El Puerto Esta Abierto":ip_cliente}
    else:
        return {"El Puerto Esta Cerrado":ip_cliente}

@user.get("/usuarios/listar",description="Get a list of all users",)
def get_usuarios(request: Request):
    api_key = request.headers.get('autorizacion')
    validatoken = validate_token(api_key)
    # if not Validar_Token(api_key):
    if not validatoken:
        return JSONResponse({'mensaje': 'Token  inválido'}), 401
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM db_usuarios"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return JSONResponse(result)




@user.get("/usuarios/lista/{id}",description="Get a single user by Id",)
def get_user(id: str,request: Request):
    api_key = request.headers.get('autorizacion')
    if not Validar_Token(api_key):
        return JSONResponse({'mensaje': 'API Key inválida'}), 401
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM db_usuarios WHERE id_usuario=%s"
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return JSONResponse(result)


@user.post("/usuarios/crear", description="Create a new user")
def crear_usuario(request: Request,payload: Usuarios):
    api_key = request.headers.get('autorizacion')
    if not Validar_Token(api_key):
        return JSONResponse({'mensaje': 'API Key inválida'}), 401
    usu = jsonable_encoder(payload)
    passhash = generate_password_hash(usu['password'])
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO db_usuarios(tipo_documento,numero_documento,nombres,apellidos,departamento,municipio,usuario, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (usu['tipo_documento'],usu['numero_documento'],usu['nombres'],usu['apellidos'],usu['departamento'],usu['municipio'],usu['usuario'], passhash))
    connection.commit()
    cursor.close()
    connection.close()
    return JSONResponse({'message': 'Usuario created successfully.'}), 201

@user.put("/usuarios/actualizar", description="Create a new user")
def create_client(request: Request,payload: Usuarios):
    api_key = request.headers.get('autorizacion')
    if not Validar_Token(api_key):
        return JSONResponse({'mensaje': 'API Key inválida'}), 401
    usuario = jsonable_encoder(payload)
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "CALL create_client_proc(%s, %s)"
    cursor.execute(query, (usuario['name'], usuario['email']))
    connection.commit()
    cursor.close()
    connection.close()
    return JSONResponse({'message': 'Usuario created successfully.'}), 201