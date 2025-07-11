import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv() # Cargar variables de entorno desde .env (para desarrollo local)

# Obtener las variables de entorno para la conexión a la base de datos.
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'huellasdb')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))

print(f"Conectando a MySQL en {MYSQL_HOST}:{MYSQL_PORT}...")

conn = None # Inicializar conn para el bloque finally
cursor = None # Inicializar cursor para el bloque finally

try:
    conn = mysql.connector.connect(
        host=MYSQL_HOST, # Usar variable de entorno para el host
        user=MYSQL_USER, # Usar variable de entorno para el usuario
        password=MYSQL_PASSWORD, # Usar variable de entorno para la contraseña
        port=MYSQL_PORT # Usar variable de entorno para el puerto
    )
    
    print("Conexión exitosa a MySQL (sin especificar DB inicial)")
    
    cursor = conn.cursor()
    database_name = MYSQL_DATABASE # Usar la variable de entorno MYSQL_DATABASE
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}`")
    print(f"Base de datos '{database_name}' creada/verificada")
    cursor.execute(f"USE `{database_name}`")
    print(f"Usando base de datos '{database_name}'")
    # Deshabilitar temporalmente las comprobaciones de clave foránea para la eliminación/creación
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    print("Comprobaciones de clave foránea deshabilitadas temporalmente.")
    # Definiciones de tablas con nombres en minúsculas y todas las restricciones
    # Incluye DROP TABLE IF EXISTS para asegurar una recreación limpia
    tables_to_create = [
        ("marca", """
        DROP TABLE IF EXISTS marca;
        CREATE TABLE marca (
            id_marca INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(50) UNIQUE
        )
        """),
        ("modelo", """
        DROP TABLE IF EXISTS modelo;
        CREATE TABLE modelo (
            id_modelo INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) UNIQUE
        )
        """),
        ("categoria", """
        DROP TABLE IF EXISTS categoria;
        CREATE TABLE categoria (
            id_categoria INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(50) UNIQUE
        )
        """),
        ("colores", """
        DROP TABLE IF EXISTS colores;
        CREATE TABLE colores (
            id_color INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(50) UNIQUE
        )
        """),
        ("cuadrante", """
        DROP TABLE IF EXISTS cuadrante;
        CREATE TABLE cuadrante (
            id_cuadrante INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(50) UNIQUE
        )
        """),
        ("formageometrica", """
        DROP TABLE IF EXISTS formageometrica;
        CREATE TABLE formageometrica (
            id_forma INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(50) UNIQUE
        )
        """),
        ("usuarios", """
        DROP TABLE IF EXISTS usuarios;
        CREATE TABLE usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(128) NOT NULL,
            role VARCHAR(20) NOT NULL
        )
        """),
        ("calzado", """
        DROP TABLE IF EXISTS calzado;
        CREATE TABLE calzado (
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
        DROP TABLE IF EXISTS calzado_color;
        CREATE TABLE calzado_color (
            id_calzado INT,
            id_color INT,
            PRIMARY KEY (id_calzado, id_color),
            FOREIGN KEY (id_calzado) REFERENCES calzado(id_calzado) ON DELETE CASCADE,
            FOREIGN KEY (id_color) REFERENCES colores(id_color) ON DELETE CASCADE
        )
        """),
        ("suela", """
        DROP TABLE IF EXISTS suela;
        CREATE TABLE suela (
            id_suela INT AUTO_INCREMENT PRIMARY KEY,
            id_calzado INT,
            descripcion_general TEXT,
            FOREIGN KEY (id_calzado) REFERENCES calzado(id_calzado) ON DELETE CASCADE
        )
        """),
        ("detallesuela", """
        DROP TABLE IF EXISTS detallesuela;
        CREATE TABLE detallesuela (
            id_detalle INT AUTO_INCREMENT PRIMARY KEY,
            id_suela INT,
            id_cuadrante INT,
            id_forma INT,
            detalle_adicional TEXT,
            FOREIGN KEY (id_suela) REFERENCES suela(id_suela) ON DELETE CASCADE,
            FOREIGN KEY (id_cuadrante) REFERENCES cuadrante(id_cuadrante) ON DELETE CASCADE,
            FOREIGN KEY (id_forma) REFERENCES formageometrica(id_forma) ON DELETE CASCADE
        )
        """),
        ("imputado", """
        DROP TABLE IF EXISTS imputado;
        CREATE TABLE imputado (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            dni VARCHAR(20) NOT NULL UNIQUE,
            direccion VARCHAR(200),
            comisaria VARCHAR(100),
            jurisdiccion VARCHAR(100)
        )
        """),
        ("calzado_has_imputado", """
        DROP TABLE IF EXISTS calzado_has_imputado;
        CREATE TABLE calzado_has_imputado (
          calzado_id_calzado INT NOT NULL,
          imputado_id INT NOT NULL,
          PRIMARY KEY (calzado_id_calzado, imputado_id),
          FOREIGN KEY (calzado_id_calzado)
            REFERENCES calzado(id_calzado)
            ON DELETE CASCADE,
          FOREIGN KEY (imputado_id)
            REFERENCES imputado(id)
            ON DELETE CASCADE
        )
        """)
    ]
    # Ejecutar las sentencias DROP y CREATE
    for table_name, create_sql in tables_to_create:
        # Ejecutar cada sentencia SQL individualmente
        for statement in create_sql.split(';'):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
        print(f"Tabla '{table_name}' eliminada y creada/verificada.")
    conn.commit()
    print("Todas las tablas creadas correctamente.")
    
except Exception as e:
    print(f"Error: {e}")
    raise
finally:
    if conn and conn.is_connected():
        try:
            if cursor:
                # Habilitar nuevamente las comprobaciones de clave foránea
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
                print("Comprobaciones de clave foránea habilitadas nuevamente.")
                cursor.close()
        except mysql.connector.Error as err:
            print(f"Error al re-habilitar FOREIGN_KEY_CHECKS o cerrar cursor: {err}")
        finally:
            conn.close()
            print("Conexión cerrada.")
