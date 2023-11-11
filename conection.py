import mysql.connector

def get_db_connection():
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'ted127'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'semillero'

    mydb = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

    return mydb
