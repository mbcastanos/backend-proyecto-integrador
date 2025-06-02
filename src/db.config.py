import MySQLdb


def get_connection():
    return MySQLdb.connect(
        host="localhost",
        user="root",
        password="1234",  # Cambiá esto por tu clave real
        database="calzado",
    )
