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

@suela_bp.route("/<int:id>", methods=["GET"])
def get_suela_by_id(id):
    try:
        if id <= 0:
            return jsonify({"Error":"ID inválido"}),400
        
        suela = Suela.query.get(id)
        
        if suela is None:
            return jsonify({"Error":"Suela no encontrada"}),404
            
        return jsonify({
            "id_suela":suela.id_suela,
            "id_calzado":suela.id_calzado,
            "descripcion":suela.descripcion_general
        })
    
    except Exception as e:
        return jsonify({"Error":str(e)})

@suela_bp.route("/", methods=["GET"])
def get_all_suelas():
    try:
        suelas = Suela.query.all() 
        suelas_list = [suela.to_dict() for suela in suelas]
        return jsonify(suelas_list), 200 # Codigo de estado 200 OK
    except Exception as e:
        # Manejo de errores para cualquier problema al consultar la base de datos
        return jsonify({"message": "Error al obtener todas las suelas", "error": str(e)}), 500

#Por simplicidad, este PUT solo actualizara los campos directos de la suela.
@suela_bp.route("/<int:id_suela>", methods=["PUT"])
def update_suela(id_suela):
    try:
        suela = Suela.query.get(id_suela)
        
        # Si no se encuentra la suela, devuelve un error 404
        if suela is None:
            return jsonify({"message": "Suela no encontrada"}), 404
        
        data = request.get_json()

        # Si no se reciben datos JSON, devuelve un error 400
        if not data:
            return jsonify({"message": "No se recibieron datos JSON para la actualizacion"}), 400

        if "id_calzado" in data:
            # Verifica que el id_calzado exista en la tabla Calzado
            from models.calzado import Calzado
            if Calzado.query.get(data["id_calzado"]) is None:
                return jsonify({"message": "id_calzado no valido. El calzado no existe."}), 400
            suela.id_calzado = data["id_calzado"]

        if "descripcion_general" in data:
            suela.descripcion_general = data["descripcion_general"]

        db.session.commit()

        return jsonify({
            "message": "Suela actualizada exitosamente",
            "suela": suela.to_dict()
        }), 200

    except Exception as e:
        # En caso de error, deshacer la transaccion y devolver un error 500
        db.session.rollback()
        return jsonify({"message": "Error al actualizar la suela", "error": str(e)}), 500