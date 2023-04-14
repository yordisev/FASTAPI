
# from conexion import create_db_connection

def Validar_Token(api_key):
    # connection = create_db_connection()
    # cursor = connection.cursor(dictionary=True)
    # query = "SELECT * FROM clients WHERE id=%s"
    # cursor.execute(query, (api_key,))
    # result = cursor.fetchone()
    # cursor.close()
    # connection.close()
    # if api_key == result:
    if api_key == '12345':
        return True
    else:
        return False