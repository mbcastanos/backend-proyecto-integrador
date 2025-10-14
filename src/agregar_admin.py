import MySQLdb
import bcrypt
import os
from dotenv import load_dotenv


load_dotenv()

def get_connection():
    MYSQL_HOST = os.getenv("MYSQL_HOST", "shinkansen.proxy.rlwy.net")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "HjdAknefMPIFscvdwvERRnzeCFgoojlW")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "railway")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 11692))

    try:
        conn = MySQLdb.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQL_PORT
        )
        print(f"Conexión exitosa a la base de datos: {MYSQL_DATABASE} en {MYSQL_HOST}:{MYSQL_PORT}")
        return conn
    except MySQLdb.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise # Re-lanzar la excepción para ver el error completo

def crear_admin():
    username = "admin"
    password = "admin123" # Contraseña por defecto para el admin
    role = "admin"

    # Hashear la contraseña antes de almacenarla
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    conn = None # Inicializar para el bloque finally
    cursor = None # Inicializar para el bloque finally

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Verificar si el usuario ya existe para evitar duplicados
        # ¡IMPORTANTE! El nombre de la tabla 'usuarios' debe ser en minúsculas
        cursor.execute("SELECT id FROM usuarios WHERE username = %s", (username,))
        if cursor.fetchone():
            print(f"El usuario '{username}' ya existe. No se creará de nuevo.")
        else:
            # Insertar el nuevo usuario administrador
            # ¡IMPORTANTE! El nombre de la tabla 'usuarios' debe ser en minúsculas
            cursor.execute(
                "INSERT INTO usuarios (username, password_hash, role) VALUES (%s, %s, %s)",
                (username, password_hash, role),
            )
            conn.commit()
            print(f"Usuario admin '{username}' creado correctamente.")

    except MySQLdb.Error as e:
        print(f"Error al crear el usuario admin: {e}")
        if conn:
            conn.rollback() # Deshacer cambios si hay un error
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    crear_admin()
