from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from flasgger import Swagger
from swagger_spec import SWAGGER_SPEC
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
    app.run(host="0.0.0.0", debug=True)
