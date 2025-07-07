import MySQLdb
import bcrypt

def get_connection():
    import os
    return MySQLdb.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "huellasdb"),
    )

def crear_admin():
    username = "admin"
    password = "admin123"
    role = "admin"

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE username = %s", (username,))
    if cursor.fetchone():
        print(f"El usuario '{username}' ya existe.")
    else:
        cursor.execute(
            "INSERT INTO usuarios (username, password_hash, role) VALUES (%s, %s, %s)",
            (username, password_hash, role),
        )
        conn.commit()
        print(f"Usuario admin '{username}' creado correctamente.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    crear_admin()