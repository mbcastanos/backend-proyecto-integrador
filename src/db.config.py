import MySQLdb


def get_connection():
    return MySQLdb.connect(
        host="admin",
        user="root",
        password="admin",  # Cambiá esto por tu clave real
        database="huellas_db",
    )
