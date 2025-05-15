import MySQLdb


def get_connection():
    return MySQLdb.connect(
        host="localhost",
        user="root",
        password="tu_contraseña",  # Cambiá esto por tu clave real
        database="crud_tareas",
    )
