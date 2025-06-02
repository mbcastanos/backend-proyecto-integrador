from flask import Flask, jsonify, Blueprint
from models import (
    db,
    Calzado,
    Suela,
    DetalleSuela,
)  # Se importaron Suela y DetalleSuela
from controllers.calzado_controller import calzado_bp
from controllers.suela_controller import suela_bp
from controllers.forma_geometrica_controller import forma_bp

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+mysqlconnector://root:admin@localhost:3306/huellasdb"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(calzado_bp)
app.register_blueprint(suela_bp)
app.register_blueprint(forma_bp)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)

   