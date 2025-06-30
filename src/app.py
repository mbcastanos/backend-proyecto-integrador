from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from flasgger import Swagger
from models import db, Calzado, Suela, DetalleSuela
from controllers.calzado_controller import calzado_bp
from controllers.suela_controller import suela_bp
from controllers.forma_geometrica_controller import forma_bp
from controllers.login_controller import login_bp
from controllers.marca_controller import marca_bp
from controllers.modelo_controller import modelo_bp
from controllers.categoria_controller import categoria_bp
from controllers.color_controller import color_bp
from controllers.imputados_controller import imputados_bp

app = Flask(__name__)

CORS(app, origins=[
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",  
    "http://127.0.0.1:5173"
], supports_credentials=True)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+mysqlconnector://root:@localhost:3306/huellasdb"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# --- Configuracion de Flasgger ---
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "title": "API del Trabajo Practico Integrador: Gestion de Huellas de Calzado",
    "specs_route": "/apidocs/"
}

# --- Definiciones de Modelos para Flasgger ---
swagger_config["definitions"] = {
    "Calzado": {
        "type": "object",
        "properties": {
            "id_calzado": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único del calzado"},
            "talle": {"type": "string", "maxLength": 10, "nullable": True, "description": "Talle del calzado"},
            "ancho": {"type": "number", "format": "float", "nullable": True, "description": "Ancho del calzado"},
            "alto": {"type": "number", "format": "float", "nullable": True, "description": "Alto del calzado"},
            "tipo_registro": {
                "type": "string",
                "enum": ["indubitada_proveedor", "indubitada_comisaria", "dubitada"],
                "nullable": True,
                "description": "Tipo de registro del calzado"
            },
            "id_marca": {"type": "integer", "format": "int32", "nullable": True, "description": "ID de la marca (clave foránea)"},
            "marca": {"type": "string", "nullable": True, "description": "Nombre de la marca (para respuestas GET)"},
            "id_modelo": {"type": "integer", "format": "int32", "nullable": True, "description": "ID del modelo (clave foránea)"},
            "modelo": {"type": "string", "nullable": True, "description": "Nombre del modelo (para respuestas GET)"},
            "id_categoria": {"type": "integer", "format": "int32", "nullable": True, "description": "ID de la categoría (clave foránea)"},
            "categoria": {"type": "string", "nullable": True, "description": "Nombre de la categoría (para respuestas GET)"},
            "colores": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Lista de nombres de colores asociados al calzado (para respuestas GET)"
            }
        },
        "required": [
            "talle",
            "ancho",
            "alto",
            "id_categoria",
            "id_marca",
            "id_modelo",
            "id_colores"
        ]
    },
    "CalzadoInput": { # Schema para la entrada POST/PATCH de Calzado
        "type": "object",
        "properties": {
            "talle": {"type": "string", "maxLength": 10, "nullable": True},
            "ancho": {"type": "number", "format": "float", "nullable": True},
            "alto": {"type": "number", "format": "float", "nullable": True},
            "tipo_registro": {
                "type": "string",
                "enum": ["indubitada_proveedor", "indubitada_comisaria", "dubitada"],
                "nullable": True
            },
            "id_marca": {"type": "integer", "format": "int32", "nullable": True},
            "id_modelo": {"type": "integer", "format": "int32", "nullable": True},
            "id_categoria": {"type": "integer", "format": "int32", "nullable": True},
            "id_colores": {
                "type": "array",
                "items": {"type": "integer", "format": "int32"},
                "description": "Lista de IDs de colores para asociar"
            }
        },
        "required": [
            "id_calzado", # Siempre presente en una respuesta
            "talle",
            "ancho",
            "alto",
            "id_marca",
            "id_modelo",
            "id_categoria",
            "colores", # Si siempre se espera que la lista de colores este presente (aunque puede estar vacia)
            "fecha_creacion",
            "ultima_actualizacion"
        ]
    },
    "Suela": {
        "type": "object",
        "properties": {
            "id_suela": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único de la suela"},
            "id_calzado": {"type": "integer", "format": "int32", "description": "ID del calzado al que pertenece la suela", "nullable": False},
            "descripcion_general": {"type": "string", "nullable": True, "description": "Descripción general de la suela"},
            "detalles": {
                "type": "array",
                "items": {"$ref": "#/definitions/DetalleSuelaOutput"}, # Referencia a la definicion de detalle para salida
                "description": "Lista de detalles de la suela (para respuestas GET)"
            }
        },
        "required": ["id_calzado"]
    },
    "SuelaInput": { # Schema para la entrada POST/PUT/PATCH de Suela
        "type": "object",
        "properties": {
            "id_calzado": {"type": "integer", "format": "int32", "description": "ID del calzado al que pertenece la suela"},
            "descripcion_general": {"type": "string", "nullable": True, "description": "Descripción general de la suela"},
            "detalles": {
                "type": "array",
                "items": {"$ref": "#/definitions/DetalleSuelaInput"}, # Referencia a la definicion de detalle para entrada
                "description": "Lista de detalles de la suela"
            }
        },
        "required": ["id_calzado"]
    },
    "DetalleSuelaOutput": { # Para la salida de DetalleSuela
        "type": "object",
        "properties": {
            "id_detalle": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único del detalle de suela"},
            "id_cuadrante": {"type": "integer", "format": "int32", "description": "ID del cuadrante"},
            "cuadrante_nombre": {"type": "string", "description": "Nombre del cuadrante (si se carga en to_dict)"},
            "id_forma": {"type": "integer", "format": "int32", "description": "ID de la forma geométrica"},
            "forma_nombre": {"type": "string", "description": "Nombre de la forma geométrica (si se carga en to_dict)"},
            "detalle_adicional": {"type": "string", "nullable": True, "description": "Detalle adicional del área"}
        },
        "required": ["id_cuadrante", "id_forma"]
    },
    "DetalleSuelaInput": { # Para la entrada de DetalleSuela
        "type": "object",
        "properties": {
            "id_cuadrante": {"type": "integer", "format": "int32", "description": "ID del cuadrante"},
            "id_forma": {"type": "integer", "format": "int32", "description": "ID de la forma geométrica"},
            "detalle_adicional": {"type": "string", "nullable": True, "description": "Detalle adicional del área"}
        },
        "required": ["id_cuadrante", "id_forma"]
    },
    "FormaGeometrica": {
        "type": "object",
        "properties": {
            "id_forma": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único de la forma geométrica"},
            "nombre": {"type": "string", "maxLength": 50, "description": "Nombre de la forma geométrica"}
        },
        "required": ["nombre"]
    },
    "Cuadrante": {
        "type": "object",
        "properties": {
            "id_cuadrante": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único del cuadrante"},
            "nombre": {"type": "string", "maxLength": 50, "description": "Nombre del cuadrante"}
        },
        "required": ["nombre"]
    },
    "Usuario": {
        "type": "object",
        "properties": {
            "id": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único del usuario"},
            "username": {"type": "string", "maxLength": 50, "description": "Nombre de usuario"},
            "role": {"type": "string", "maxLength": 20, "description": "Rol del usuario (ej. 'admin', 'user')"}
            # password_hash no se expone en la API
        },
        "required": ["username", "role"]
    },
    "UsuarioInput": { # Schema para la entrada POST/PATCH de Usuario
        "type": "object",
        "properties": {
            "username": {"type": "string", "maxLength": 50, "description": "Nombre de usuario"},
            "password": {"type": "string", "description": "Contraseña (solo para creación y actualización)"},
            "role": {"type": "string", "maxLength": 20, "description": "Rol del usuario (ej. 'admin', 'user')"}
        },
        "required": ["username", "password", "role"] # password es requerido en POST
    },
    "LoginInput": {
        "type": "object",
        "properties": {
            "username": {"type": "string", "description": "Nombre de usuario"},
            "password": {"type": "string", "description": "Contraseña"}
        },
        "required": ["username", "password"]
    },
    "LoginResponse": {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "token": {"type": "string"}
        }
    },
    "Marca": {
        "type": "object",
        "properties": {
            "id_marca": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único de la marca"},
            "nombre": {"type": "string", "maxLength": 50, "description": "Nombre de la marca"}
        },
        "required": ["nombre"]
    },
    "Categoria": {
        "type": "object",
        "properties": {
            "id_categoria": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único de la categoría"},
            "nombre": {"type": "string", "maxLength": 50, "description": "Nombre de la categoría"}
        },
        "required": ["nombre"]
    },
    "Color": {
        "type": "object",
        "properties": {
            "id_color": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único del color"},
            "nombre": {"type": "string", "maxLength": 50, "description": "Nombre del color"}
        },
        "required": ["nombre"]
    },
    "Modelo": {
        "type": "object",
        "properties": {
            "id_modelo": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único del modelo"},
            "nombre": {"type": "string", "maxLength": 100, "description": "Nombre del modelo"}
        },
        "required": ["nombre"]
    },
    "MessageResponse": { # Para respuestas de exito genericas
        "type": "object",
        "properties": {
            "message": {"type": "string"}
        }
    },
    "ErrorResponse": { # Para respuestas de error genericas
        "type": "object",
        "properties": {
            "error": {"type": "string"}
        }
    }
}

swagger = Swagger(app, config=swagger_config)

db.init_app(app)

app.register_blueprint(calzado_bp)
app.register_blueprint(suela_bp)
app.register_blueprint(forma_bp)
app.register_blueprint(login_bp)
app.register_blueprint(marca_bp)
app.register_blueprint(modelo_bp)
app.register_blueprint(categoria_bp)
app.register_blueprint(color_bp)
app.register_blueprint(imputados_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)
