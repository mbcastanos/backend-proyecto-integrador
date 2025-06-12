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

cursor.execute("""
CREATE TABLE IF NOT EXISTS Calzado (
    id_calzado INT AUTO_INCREMENT PRIMARY KEY,
    talle VARCHAR(10),
    ancho DECIMAL(5,2),
    alto DECIMAL(5,2),
    tipo_registro ENUM('indubitada_proveedor', 'indubitada_comisaria', 'dubitada')
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Modelo (
    id_modelo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    id_calzado INT,
    FOREIGN KEY (id_calzado) REFERENCES Calzado(id_calzado)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS colores (
    id_color INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    id_calzado INT,
    FOREIGN KEY (id_calzado) REFERENCES Calzado(id_calzado)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    id_calzado INT,
    FOREIGN KEY (id_calzado) REFERENCES Calzado(id_calzado)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Marca (
    id_marca INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    id_calzado INT,
    FOREIGN KEY (id_calzado) REFERENCES Calzado(id_calzado)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS User (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    user VARCHAR(50),
    contraseña VARCHAR(50)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Suela (
    id_suela INT AUTO_INCREMENT PRIMARY KEY,
    id_calzado INT,
    descripcion_general TEXT,
    FOREIGN KEY (id_calzado) REFERENCES Calzado(id_calzado)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Cuadrante (
    id_cuadrante INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS FormaGeometrica (
    id_forma INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS DetalleSuela (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_suela INT,
    id_cuadrante INT,
    id_forma INT,
    detalle_adicional TEXT,
    FOREIGN KEY (id_suela) REFERENCES Suela(id_suela),
    FOREIGN KEY (id_cuadrante) REFERENCES Cuadrante(id_cuadrante),
    FOREIGN KEY (id_forma) REFERENCES FormaGeometrica(id_forma)
)
""")

conn.commit()
conn.close()