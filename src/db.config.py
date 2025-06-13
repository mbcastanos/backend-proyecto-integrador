import MySQLdb


def get_connection():
    return MySQLdb.connect(
        host="admin",
        user="root",
        password="tuclave",  # Cambiá esto por tu clave real
        database="calzado",
    )
