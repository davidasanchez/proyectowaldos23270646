import mysql.connector

def crear_conexion():
    return mysql.connector.connect(
        host='localhost',
        user='root',         # Cambia por tu usuario MySQL
        password='david1234', # Cambia por tu password MySQL
        database='walditos'
    )