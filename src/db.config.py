import MySQLdb


def get_connection():
    return MySQLdb.connect(
        host="admin",
        user="root",
        password="root",  # Cambiá esto por tu clave real
        database="huelladb",
    )
