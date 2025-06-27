from flask import Flask, jsonify, Blueprint
from models import db, Calzado, Suela, DetalleSuela
from controllers.calzado_controller import calzado_bp
from controllers.suela_controller import suela_bp
from controllers.forma_geometrica_controller import forma_bp
from controllers.login_controller import login_bp
from controllers.marca_controller import marca_bp
from controllers.modelo_controller import modelo_bp
from controllers.categoria_controller import categoria_bp
from controllers.color_controller import color_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+mysqlconnector://root:1234@localhost:3306/huellas_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(calzado_bp)
app.register_blueprint(suela_bp)
app.register_blueprint(forma_bp)
app.register_blueprint(login_bp)
app.register_blueprint(marca_bp)
app.register_blueprint(modelo_bp)
app.register_blueprint(categoria_bp)
app.register_blueprint(color_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)
