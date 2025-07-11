import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

# Obtener las variables de entorno para la conexión a la base de datos
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'huellasdb')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))

print(f"Conectando a MySQL en puerto {MYSQL_PORT}...")

try:
    conn = mysql.connector.connect(
        host = MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=MYSQL_PORT
    )
    print("Conexión exitosa a MySQL")
    
    cursor = conn.cursor()
    database_name = MYSQL_DATABASE
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    print(f"Base de datos '{database_name}' creada/verificada")

    cursor.execute(f"USE {database_name}")
    print(f"Usando base de datos '{database_name}'")

    tables = [
        ("marca", """
        CREATE TABLE IF NOT EXISTS marca (
            id_marca INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(50) UNIQUE
        )
        """),
        ("modelo", """
        CREATE TABLE IF NOT EXISTS modelo (
            id_modelo INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) UNIQUE
        )
        """),
        ("categoria", """
        CREATE TABLE IF NOT EXISTS categoria (
            id_categoria INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(50) UNIQUE
        )
        """),
        ("colores", """
        CREATE TABLE IF NOT EXISTS colores (
            id_color INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(50) UNIQUE
        )
        """),
        ("cuadrante", """
        CREATE TABLE IF NOT EXISTS cuadrante (
            id_cuadrante INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(50)
        )
        """),
        ("formageometrica", """
        CREATE TABLE IF NOT EXISTS formageometrica (
            id_forma INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(50)
        )
        """),
        ("usuarios", """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(128) NOT NULL,
            role VARCHAR(20) NOT NULL
        )
        """),
        ("calzado", """
        CREATE TABLE IF NOT EXISTS calzado (
            id_calzado INT AUTO_INCREMENT PRIMARY KEY,
            talle VARCHAR(10),
            ancho DECIMAL(5,2),
            alto DECIMAL(5,2),
            tipo_registro ENUM('indubitada_proveedor', 'indubitada_comisaria', 'dubitada'),
            id_marca INT,
            id_modelo INT,
            id_categoria INT,
            FOREIGN KEY (id_marca) REFERENCES marca(id_marca),
            FOREIGN KEY (id_modelo) REFERENCES modelo(id_modelo),
            FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria)
        )
        """),
        ("calzado_color", """
        CREATE TABLE IF NOT EXISTS calzado_color (
            id_calzado INT,
            id_color INT,
            PRIMARY KEY (id_calzado, id_color),
            FOREIGN KEY (id_calzado) REFERENCES calzado(id_calzado) ON DELETE CASCADE,
            FOREIGN KEY (id_color) REFERENCES colores(id_color) ON DELETE CASCADE
        )
        """),
        ("suela", """
        CREATE TABLE IF NOT EXISTS suela (
            id_suela INT AUTO_INCREMENT PRIMARY KEY,
            id_calzado INT,
            descripcion_general TEXT,
            FOREIGN KEY (id_calzado) REFERENCES calzado(id_calzado)
        )
        """),
        ("detallesuela", """
        CREATE TABLE IF NOT EXISTS detallesuela (
            id_detalle INT AUTO_INCREMENT PRIMARY KEY,
            id_suela INT,
            id_cuadrante INT,
            id_forma INT,
            detalle_adicional TEXT,
            FOREIGN KEY (id_suela) REFERENCES suela(id_suela),
            FOREIGN KEY (id_cuadrante) REFERENCES cuadrante(id_cuadrante),
            FOREIGN KEY (id_forma) REFERENCES formageometrica(id_forma)
        )
        """),
          ("imputados", """
        CREATE TABLE IF NOT EXISTS imputado (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            dni INT NOT NULL,
            direccion VARCHAR(100) NOT NULL,
            comisaria VARCHAR(100) NOT NULL,
            jurisdiccion VARCHAR(100) NOT NULL
        )
        """)
    ]

    for table_name, create_sql in tables:
        cursor.execute(create_sql)
        print(f"Tabla '{table_name}' creada/verificada")

    conn.commit()
    print("Todas las tablas creadas correctamente.")
    
except Exception as e:
    print(f"Error: {e}")
    raise
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("Conexión cerrada.")
