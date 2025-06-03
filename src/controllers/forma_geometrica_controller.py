from flask import Blueprint, jsonify, request
from models import db, FormaGeometrica

forma_bp = Blueprint("forma_bp", __name__)


@forma_bp.route("/formas", methods=["GET"])
def get_all_formas():
    formas = FormaGeometrica.query.all()
    return jsonify([{"id_forma": f.id_forma, "nombre": f.nombre} for f in formas])


@forma_bp.route("/formas", methods=["POST"])
def create_forma():
    data = request.get_json()
    nombre = data.get("nombre")

    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400

    nueva_forma = FormaGeometrica(nombre=nombre)
    db.session.add(nueva_forma)
    db.session.commit()

    return (
        jsonify({"mensaje": "Forma creada con éxito", "id": nueva_forma.id_forma}),
        201,
    )
