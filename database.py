import mysql.connector

def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pythoncurd"
    )