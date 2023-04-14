import mysql.connector

def create_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_python",
        port=3306
    )
    return connection