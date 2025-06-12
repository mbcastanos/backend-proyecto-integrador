import MySQLdb


def get_connection():
    return MySQLdb.connect(
        host="admin",
        user="root",
        password="1234",  # Cambiá esto por tu clave real
        database="calzado",
    )
