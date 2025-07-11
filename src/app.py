from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from flasgger import Swagger
from src.swagger_spec import SWAGGER_SPEC
from src.models import db, Calzado, Suela, DetalleSuela
from src.controllers.calzado_controller import calzado_bp
from src.controllers.suela_controller import suela_bp
from src.controllers.forma_geometrica_controller import forma_bp
from src.controllers.login_controller import login_bp
from src.controllers.marca_controller import marca_bp
from src.controllers.modelo_controller import modelo_bp
from src.controllers.categoria_controller import categoria_bp
from src.controllers.color_controller import color_bp
from src.controllers.imputados_controller import imputados_bp
import os
from dotenv import load_dotenv

load_dotenv()

# Obtener las variables de entorno para la conexión a la base de datos
MYSQL_HOST = os.getenv('MYSQL_HOST', 'gondola.proxy.rlwy.net')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'LPibeCJDBWxROkNbNaAtDYrvfyXBKIyz')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'railway')
MYSQL_PORT = os.getenv('MYSQL_PORT', '35908')


app = Flask(__name__)

frontend_origins_str = os.getenv("FRONTEND_URL", "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173,https://huellasfrontend.vercel.app")
allowed_origins = [origin.strip() for origin in frontend_origins_str.split(',')]
CORS(app, origins=allowed_origins, supports_credentials=True)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configuracion de Flasgger
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
    "specs_route": "/apidocs/",
    # diccionario SWAGGER_SPEC importado para todas las definiciones y rutas
    **SWAGGER_SPEC
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
    debug_mode = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(host="0.0.0.0", debug=debug_mode)
