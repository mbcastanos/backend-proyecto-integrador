from flask import Blueprint, jsonify, request
from models import db, Suela, DetalleSuela

suela_bp = Blueprint("suela_bp", __name__, url_prefix="/suelas")


@suela_bp.route("/", methods=["POST"])
def create_suela():
    try:
        data = request.get_json()
        nueva_suela = Suela(
            id_calzado=data["id_calzado"],
            descripcion_general=data.get("descripcion_general", ""),
        )
        db.session.add(nueva_suela)
        db.session.flush()  # Para obtener el ID generado

        for detalle in data.get("detalles", []):
            nuevo_detalle = DetalleSuela(
                id_suela=nueva_suela.id_suela,
                id_cuadrante=detalle["id_cuadrante"],
                id_forma=detalle["id_forma"],
                detalle_adicional=detalle.get("detalle_adicional", ""),
            )
            db.session.add(nuevo_detalle)

        db.session.commit()
        return (
            jsonify(
                {"msg": "Suela creada exitosamente", "id_suela": nueva_suela.id_suela}
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
