import os
import mysql.connector
from dotenv import load_dotenv
import bcrypt

load_dotenv() # Cargar variables de entorno desde .env (para desarrollo local)

# Obtener las variables de entorno para la conexión a la base de datos
# Se usan los nombres de variables con prefijo MYSQL_ según tu configuración.
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '') # Asegúrate de que esta variable tenga el valor correcto en Railway/local
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'huellasdb') # Valor por defecto para local, en Railway debe ser 'railway'
MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))

print(f"Conectando a MySQL en {MYSQL_HOST}:{MYSQL_PORT}...")

conn = None # Inicializar conn para el bloque finally
cursor = None # Inicializar cursor para el bloque finally

try:
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=MYSQL_PORT
    )
    print("Conexión exitosa a MySQL (sin especificar DB inicial)")
    
    cursor = conn.cursor()
    
    database_name = MYSQL_DATABASE # Usar la variable de entorno MYSQL_DATABASE
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}`")
    print(f"Base de datos '{database_name}' creada/verificada")
    
    cursor.execute(f"USE `{database_name}`")
    print(f"Usando base de datos '{database_name}'")
    
except Exception as e:
    print(f"Error al conectar a MySQL o crear/usar DB: {e}")
    raise
finally:
    # Asegurarse de que la conexión se cierre si hay un error antes de continuar
    if conn and conn.is_connected():
        if cursor:
            cursor.close()
        conn.close()
        print("Conexión inicial cerrada para reabrir con la DB correcta.")

# Reabrir la conexión, esta vez especificando la base de datos directamente
try:
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        port=MYSQL_PORT
    )
    cursor = conn.cursor()
    print(f"Conexión exitosa a la base de datos '{MYSQL_DATABASE}'")

    print("Verificando y ejecutando seed (insertando datos iniciales si no existen)...")

    # --- Inserción de datos ---
    # Asegúrate de que las tablas estén creadas antes de insertar datos.
    # En un flujo de despliegue, setup_db.py se ejecutaría primero.

    # Insertar usuarios
    usuarios = [
        ("admin", "admin123", "admin"),
        ("usuario1", "password123", "user"),
        ("analista", "analista123", "analyst")
    ]

    for username, password, role in usuarios:
        # Usar SELECT COUNT(*) para verificar si el usuario ya existe
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE username = %s", (username,))
        if cursor.fetchone()[0] == 0: # Solo insertar si el usuario no existe
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8")
            cursor.execute("""
                INSERT INTO usuarios (username, password_hash, role)
                VALUES (%s, %s, %s)
            """, (username, hashed, role))
            conn.commit() # Commit individual para usuarios
            print(f"Usuario '{username}' insertado.")
        else:
            print(f"Usuario '{username}' ya existe, omitiendo inserción.")

    # Insertar cuadrantes
    cursor.execute("SELECT COUNT(*) FROM cuadrante")
    if cursor.fetchone()[0] == 0:
        print("Insertando cuadrantes...")
        cuadrantes = [
            "Cuadrante Superior Izquierdo",
            "Cuadrante Superior Derecho",
            "Cuadrante Inferior Izquierdo",
            "Cuadrante Inferior Derecho",
            "Cuadrante Central"
        ]
        for nombre in cuadrantes:
            cursor.execute("INSERT IGNORE INTO cuadrante (nombre) VALUES (%s)", (nombre,))
        conn.commit()
        print("Cuadrantes insertados.")
    else:
        print("La tabla 'cuadrante' ya contiene datos.")

    # Insertar formas geométricas
    cursor.execute("SELECT COUNT(*) FROM formageometrica")
    if cursor.fetchone()[0] == 0:
        print("Insertando formas geométricas...")
        formas = ["Círculo", "Rombo", "Pirámide", "Texto", "Logo", "Triángulo", "Rectángulo"]
        for forma in formas:
            cursor.execute("INSERT IGNORE INTO formageometrica (nombre) VALUES (%s)", (forma,))
        conn.commit()
        print("Formas geométricas insertadas.")
    else:
        print("La tabla 'formageometrica' ya contiene datos.")

    # Insertar modelos
    cursor.execute("SELECT COUNT(*) FROM modelo")
    if cursor.fetchone()[0] == 0:
        print("Insertando modelos...")
        modelos = [
            "Air Zoom", "Superstar", "SteelToe", "Classic", "Pro Runner"
        ]
        for modelo_nombre in modelos:
            cursor.execute("""
                INSERT IGNORE INTO modelo (nombre)
                VALUES (%s)
            """, (modelo_nombre,))
        conn.commit()
        print("Modelos insertados.")
    else:
        print("La tabla 'modelo' ya contiene datos.")

    # Insertar colores
    cursor.execute("SELECT COUNT(*) FROM colores")
    if cursor.fetchone()[0] == 0:
        print("Insertando colores...")
        colores = [
            "Negro", "Blanco", "Amarillo", "Beige", "Azul", "Celeste", "Turquesa",
            "Verde", "Rojo", "Naranja", "Violeta", "Magenta", "Gris", "Rosa",
            "Bordo", "Marrón"
        ]
        for color_nombre in colores:
            cursor.execute("""
                INSERT IGNORE INTO colores (nombre)
                VALUES (%s)
            """, (color_nombre,))
        conn.commit()
        print("Colores insertados.")
    else:
        print("La tabla 'colores' ya contiene datos.")

    # Insertar categorías
    cursor.execute("SELECT COUNT(*) FROM categoria")
    if cursor.fetchone()[0] == 0:
        print("Insertando categorías...")
        categorias = [
            "Deportivo", "Urbano", "Trabajo", "Casual", "Formal"
        ]
        for categoria_nombre in categorias:
            cursor.execute("""
                INSERT IGNORE INTO categoria (nombre)
                VALUES (%s)
            """, (categoria_nombre,))
        conn.commit()
        print("Categorías insertadas.")
    else:
        print("La tabla 'categoria' ya contiene datos.")

    # Insertar marcas
    cursor.execute("SELECT COUNT(*) FROM marca")
    if cursor.fetchone()[0] == 0:
        print("Insertando marcas...")
        marcas = [
            "Nike", "Adidas", "Caterpillar", "Timberland", "Pampero", "Havaianas",
            "Converse", "Puma", "Vans", "Reebok", "New Balance", "Asics",
            "Under Armour", "Fila", "Skechers", "Hoka", "Salomon", "John Foos", "Topper"
        ]
        for marca_nombre in marcas:
            cursor.execute("""
                INSERT IGNORE INTO marca (nombre)
                VALUES (%s)
            """, (marca_nombre,))
        conn.commit()
        print("Marcas insertadas.")
    else:
        print("La tabla 'marca' ya contiene datos.")

    # --- INSERCIONES DE DATOS TRANSACCIONALES (CALZADOS, SUELAS, DETALLES, ETC.) ---
    # Estas se insertan solo si la tabla principal 'calzado' está vacía.
    # Si necesitas insertar más de un conjunto de calzados en diferentes ejecuciones,
    # necesitarías una lógica más compleja para verificar duplicados por sus atributos.

    cursor.execute("SELECT COUNT(*) FROM calzado")
    cantidad_calzados = cursor.fetchone()[0]

    if cantidad_calzados == 0:
        print("Insertando calzados y datos relacionados...")

        # Obtener IDs de las tablas independientes (después de que se hayan insertado)
        cursor.execute("SELECT id_marca FROM marca")
        marca_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id_modelo FROM modelo")
        modelo_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id_categoria FROM categoria")
        categoria_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id_color FROM colores")
        color_ids = [row[0] for row in cursor.fetchall()]

        # Asegurarse de que tenemos IDs para insertar calzados
        if not (marca_ids and modelo_ids and categoria_ids and color_ids):
            print("ADVERTENCIA: No se pudieron insertar calzados porque faltan datos de referencia (marcas, modelos, categorías, colores).")
        else:
            # Insertar calzados
            calzados_data = [
                ("42", 10.5, 28.0, "indubitada_proveedor", marca_ids[0], modelo_ids[0], categoria_ids[0]),
                ("41", 10.0, 27.5, "indubitada_comisaria", marca_ids[1], modelo_ids[1], categoria_ids[1]),
                ("43", 11.0, 29.0, "dubitada", marca_ids[2], modelo_ids[2], categoria_ids[2]),
                ("40", 9.5, 26.5, "indubitada_proveedor", marca_ids[3], modelo_ids[3], categoria_ids[3]),
                ("44", 11.5, 29.5, "dubitada", marca_ids[4], modelo_ids[4], categoria_ids[4])
            ]

            for c in calzados_data:
                cursor.execute("""
                    INSERT INTO calzado (talle, ancho, alto, tipo_registro, id_marca, id_modelo, id_categoria)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, c)
            conn.commit()
            print("Calzados insertados.")

            # Obtener IDs de calzados recién insertados
            cursor.execute("SELECT id_calzado FROM calzado")
            calzado_ids = [row[0] for row in cursor.fetchall()]

            # Tabla intermedia calzado_color
            if calzado_ids and color_ids:
                for i, calzado_id in enumerate(calzado_ids):
                    color_id = color_ids[i % len(color_ids)]
                    cursor.execute("""
                        INSERT IGNORE INTO calzado_color (id_calzado, id_color)
                        VALUES (%s, %s)
                    """, (calzado_id, color_id))
                conn.commit()
                print("Relaciones calzado-color insertadas.")
            else:
                print("ADVERTENCIA: No se pudieron insertar relaciones calzado-color.")

            # Insertar suelas para cada calzado
            if calzado_ids:
                for id_calzado in calzado_ids:
                    cursor.execute("""
                        INSERT INTO suela (id_calzado, descripcion_general)
                        VALUES (%s, %s)
                    """, (id_calzado, "Suela con dibujo estándar para pruebas"))
                conn.commit()
                print("Suelas insertadas.")
            else:
                print("ADVERTENCIA: No se pudieron insertar suelas.")

            # Obtener IDs para los detalles de suela
            cursor.execute("SELECT id_cuadrante FROM cuadrante")
            cuadrante_ids = [row[0] for row in cursor.fetchall()]

            cursor.execute("SELECT id_forma FROM formageometrica")
            forma_ids = [row[0] for row in cursor.fetchall()]

            cursor.execute("SELECT id_suela FROM suela")
            suela_ids = [row[0] for row in cursor.fetchall()]

            # Insertar detalles de suela
            if suela_ids and cuadrante_ids and forma_ids:
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
                print("Detalles de suela insertados.")
            else:
                print("ADVERTENCIA: No se pudieron insertar detalles de suela.")

            print("Datos por defecto insertados exitosamente.")
    else:
        print("La tabla 'calzado' ya contiene datos. Saltando la inserción de calzados y datos relacionados.")

except Exception as e:
    print(f"Error durante la ejecución del seed: {e}")
    raise
finally:
    if conn and conn.is_connected():
        if cursor:
            cursor.close()
        conn.close()
        print("Conexión de seed cerrada.")