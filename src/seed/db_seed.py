import os
import mysql.connector
from dotenv import load_dotenv
import bcrypt


load_dotenv()

# Obtener las variables de entorno para la conexión a la base de datos
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'huellasdb')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))

print(f"MYSQL_PORT: {MYSQL_PORT}")
print(f"MYSQL_DATABASE: {MYSQL_DATABASE}")
print(f"Host: {MYSQL_HOST}")
print(f"User: {MYSQL_USER}")

try:
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
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
    
except Exception as e:
    print(f"Error al conectar a MySQL: {e}")
    raise

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM Calzado")
cantidad = cursor.fetchone()[0]

if cantidad > 0:
    print("Seed ya ejecutado.")
else:
    print("Ejecutando seed...")

usuarios = [
    ("admin", "admin123", "admin"),
    ("usuario1", "password123", "user"),
    ("analista", "analista123", "analyst")
]

# Itera sobre una lista de usuarios, verifica si cada usuario existe en la DB;
# si no, hashea la contraseña y lo inserta en la tabla 'Usuarios'.
for username, password, role in usuarios:
    cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE username = %s", (username,))
    if cursor.fetchone()[0] == 0:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8")
        cursor.execute("""
            INSERT INTO usuarios (username, password_hash, role)
            VALUES (%s, %s, %s)
        """, (username, hashed, role))

    # Insertar cuadrantes
    cuadrantes = [
        "Cuadrante Superior Izquierdo",
        "Cuadrante Superior Derecho",
        "Cuadrante Inferior Izquierdo",
        "Cuadrante Inferior Derecho",
        "Cuadrante Central"
    ]

    for nombre in cuadrantes:
        cursor.execute("INSERT INTO cuadrante (nombre) VALUES (%s)", (nombre,))

    # Insertar formas geométricas
    formas = ["Círculo", "Rombo", "Pirámide", "Texto", "Logo", "Triángulo", "Rectángulo"]

    for forma in formas:
        cursor.execute("INSERT INTO formageometrica (nombre) VALUES (%s)", (forma,))

    # Insertar todos los modelos
    modelos = [
        "Air Zoom",
        "Superstar", 
        "SteelToe",
        "Classic",
        "Pro Runner"
    ]

    for modelo_nombre in modelos:
        cursor.execute("""
            INSERT IGNORE INTO modelo (nombre)
            VALUES (%s)
        """, (modelo_nombre,))

    # Insertar todos los colores
    colores = [
        "Negro",
        "Blanco",
        "Amarillo",
        "Beige",
        "Azul",
        "Celeste",
        "Turquesa",
        "Verde",
        "Rojo",
        "Naranja",
        "Violeta",
        "Magenta",
        "Gris",
        "Rosa",
        "Bordo",
        "Marrón"
    ]

    for color_nombre in colores:
        cursor.execute("""
            INSERT IGNORE INTO colores (nombre)
            VALUES (%s)
        """, (color_nombre,))

    # Insertar todas las categorías
    categorias = [
        "Deportivo",
        "Urbano",
        "Trabajo",
        "Casual",
        "Formal"
    ]

    for categoria_nombre in categorias:
        cursor.execute("""
            INSERT IGNORE INTO categoria (nombre)
            VALUES (%s)
        """, (categoria_nombre,))

    # Insertar todas las marcas
    marcas = [
        "Nike",
        "Adidas",
        "Caterpillar",
        "Timberland",
        "Pampero",
        "Havaianas",
        "Converse",
        "Puma",
        "Vans",
        "Reebok",
        "New Balance",
        "Asics",
        "Under Armour",
        "Fila",
        "Skechers",
        "Hoka",
        "Salomon",
        "John Foos",
        "Topper"
    ]

    for marca_nombre in marcas:
        cursor.execute("""
            INSERT IGNORE INTO marca (nombre)
            VALUES (%s)
        """, (marca_nombre,))

    # Obtener IDs de las tablas independientes
    cursor.execute("SELECT id_marca FROM marca")
    marca_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id_modelo FROM modelo")
    modelo_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id_categoria FROM categoria")
    categoria_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id_color FROM colores")
    color_ids = [row[0] for row in cursor.fetchall()]

    # Insertar calzados con referencias a las tablas independientes
    calzados = [
        ("42", 10.5, 28.0, "indubitada_proveedor", marca_ids[0], modelo_ids[0], categoria_ids[0]),
        ("41", 10.0, 27.5, "indubitada_comisaria", marca_ids[1], modelo_ids[1], categoria_ids[1]),
        ("43", 11.0, 29.0, "dubitada", marca_ids[2], modelo_ids[2], categoria_ids[2]),
        ("40", 9.5, 26.5, "indubitada_proveedor", marca_ids[3], modelo_ids[3], categoria_ids[3]),
        ("44", 11.5, 29.5, "dubitada", marca_ids[4], modelo_ids[4], categoria_ids[4])
    ]

    for c in calzados:
        cursor.execute("""
            INSERT INTO calzado (talle, ancho, alto, tipo_registro, id_marca, id_modelo, id_categoria)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, c)

    conn.commit()

    cursor.execute("SELECT id_calzado FROM calzado")
    calzado_ids = [row[0] for row in cursor.fetchall()]

    # Tabla intermedia
    for i, calzado_id in enumerate(calzado_ids):
        color_id = color_ids[i % len(color_ids)]
        cursor.execute("""
            INSERT IGNORE INTO calzado_color (id_calzado, id_color)
            VALUES (%s, %s)
        """, (calzado_id, color_id))

    conn.commit()

    # Insertar suelas para cada calzado
    for id_calzado in calzado_ids:
        cursor.execute("""
            INSERT INTO suela (id_calzado, descripcion_general)
            VALUES (%s, %s)
        """, (id_calzado, "Suela con dibujo estándar para pruebas"))

    conn.commit()

    # Obtener IDs para las relaciones
    cursor.execute("SELECT id_cuadrante FROM cuadrante")
    cuadrante_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id_forma FROM formageometrica")
    forma_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id_suela FROM suela")
    suela_ids = [row[0] for row in cursor.fetchall()]

    # Insertar detalles de suela
    for suela_id in suela_ids:
        for i in range(3): 
            cursor.execute("""
                INSERT INTO detallesuela (id_suela, id_cuadrante, id_forma, detalle_adicional)
                VALUES (%s, %s, %s, %s)
            """, (
                suela_id,
                cuadrante_ids[i % len(cuadrante_ids)],
                forma_ids[i % len(forma_ids)],
                f"Detalle de prueba {i+1}"
            ))

    conn.commit()
    print("Se han cargado los datos correctamente.")

cursor.close()
conn.close()
