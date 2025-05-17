import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv() 

conn = mysql.connector.connect(
    host="mysql",
    user="root",
    password=os.getenv("MYSQL_ROOT_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE"),
    port=int(os.getenv("MYSQL_PORT", 3306))
)
cursor = conn.cursor()

cuadrantes = [
    "Cuadrante Superior Izquierdo",
    "Cuadrante Superior Derecho",
    "Cuadrante Inferior Izquierdo",
    "Cuadrante Inferior Derecho",
    "Cuadrante Central"
]

for nombre in cuadrantes:
    cursor.execute("INSERT INTO Cuadrante (nombre) VALUES (%s)", (nombre,))

formas = ["Círculo", "Rombo", "Pirámide", "Texto", "Logo", "Triángulo", "Rectángulo"]

for forma in formas:
    cursor.execute("INSERT INTO FormaGeometrica (nombre) VALUES (%s)", (forma,))

calzados = [
    ("deportivo", "Nike", "Air Zoom", "42", 10.5, 28.0, "negro/blanco", "indubitada_proveedor"),
    ("urbano", "Adidas", "Superstar", "41", 10.0, 27.5, "blanco/negro", "indubitada_comisaria"),
    ("trabajo", "Caterpillar", "SteelToe", "43", 11.0, 29.0, "amarillo/negro", "dubitada")
]

for c in calzados:
    cursor.execute("""
        INSERT INTO Calzado (categoria, marca, modelo, talle, ancho, alto, colores, tipo_registro)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, c)

conn.commit() 

cursor.execute("SELECT id_calzado FROM Calzado")
calzado_ids = [row[0] for row in cursor.fetchall()]

for id_calzado in calzado_ids:
    cursor.execute("INSERT INTO Suela (id_calzado, descripcion_general) VALUES (%s, %s)", (
        id_calzado, "Suela con dibujo estándar para pruebas"
    ))

cursor.execute("SELECT id_cuadrante FROM Cuadrante")
cuadrante_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id_forma FROM FormaGeometrica")
forma_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id_suela FROM Suela")
suela_ids = [row[0] for row in cursor.fetchall()]

for suela_id in suela_ids:
    for i in range(3): 
        cursor.execute("""
            INSERT INTO DetalleSuela (id_suela, id_cuadrante, id_forma, detalle_adicional)
            VALUES (%s, %s, %s, %s)
        """, (
            suela_id,
            cuadrante_ids[i],
            forma_ids[i],
            "Test"
        ))

conn.commit()
cursor.close()
conn.close()

print("Se han cargado los datos correctamente.")
