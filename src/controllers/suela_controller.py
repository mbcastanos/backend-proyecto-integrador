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

        detalles = []
        for detalle in data.get("detalles", []):
            nuevo_detalle = DetalleSuela(
                id_suela=nueva_suela.id_suela,
                id_cuadrante=detalle["id_cuadrante"],
                id_forma=detalle["id_forma"],
                detalle_adicional=detalle.get("detalle_adicional", ""),
            )
            db.session.add(nuevo_detalle)
            detalles.append({
                "id_cuadrante": nuevo_detalle.id_cuadrante,
                "id_forma": nuevo_detalle.id_forma,
                "detalle_adicional": nuevo_detalle.detalle_adicional
            })
            
        db.session.commit()
        
        return jsonify({
            "msg": "Suela creada exitosamente",
            "suela": {
                "id_suela": nueva_suela.id_suela,
                "id_calzado": nueva_suela.id_calzado,
                "descripcion_general": nueva_suela.descripcion_general,
                "detalles": detalles
            }
        }), 201
        
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
        return jsonify(suelas_list), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener todas las suelas", "error": str(e)}), 500

@suela_bp.route("/<int:id_suela>", methods=["PUT"])
def update_suela(id_suela):
    try:
        suela = Suela.query.get(id_suela)
        
        if suela is None:
            return jsonify({"message": "Suela no encontrada"}), 404
        
        data = request.get_json()

        if not data:
            return jsonify({"message": "No se recibieron datos JSON para la actualizacion"}), 400

        if "id_calzado" in data:
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
        db.session.rollback()
        return jsonify({"message": "Error al actualizar la suela", "error": str(e)}), 500
    

@suela_bp.route("/<int:id_suela>", methods=["DELETE"])
def delete_suela(id_suela):
    try:
        suela = Suela.query.get(id_suela)
        
        if suela is None:
            return jsonify({"message": "Suela no encontrada"}), 404
        
        db.session.delete(suela)
        db.session.commit()
        
        return jsonify({"message": "Suela eliminada exitosamente"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error al eliminar la suela", "error": str(e)}), 500

@suela_bp.route("/<int:id_suela>/partial", methods=["PATCH"])
def partial_update_suela(id_suela):
    try:
        suela = Suela.query.get(id_suela)
        if suela is None:
            return jsonify({"message": "Suela no encontrada"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"message": "No se recibieron datos JSON para la actualización"}), 400

        if "id_calzado" in data:
            from models.calzado import Calzado
            if Calzado.query.get(data["id_calzado"]) is None:
                return jsonify({"message": "id_calzado no válido. El calzado no existe."}), 400
            suela.id_calzado = data["id_calzado"]

        if "descripcion_general" in data:
            suela.descripcion_general = data["descripcion_general"]

        detalles = []
        if "detalles" in data:
            DetalleSuela.query.filter_by(id_suela=id_suela).delete()
            for detalle in data.get("detalles", []):
                nuevo_detalle = DetalleSuela(
                    id_suela=id_suela,
                    id_cuadrante=detalle["id_cuadrante"],
                    id_forma=detalle["id_forma"],
                    detalle_adicional=detalle.get("detalle_adicional", "")
                )
                db.session.add(nuevo_detalle)
                detalles.append({
                    "id_cuadrante": nuevo_detalle.id_cuadrante,
                    "id_forma": nuevo_detalle.id_forma,
                    "detalle_adicional": nuevo_detalle.detalle_adicional
                })

        db.session.commit()

        return jsonify({
            "message": "Suela actualizada parcialmente con éxito",
            "suela": {
                "id_suela": suela.id_suela,
                "id_calzado": suela.id_calzado,
                "descripcion_general": suela.descripcion_general,
                "detalles": detalles if "detalles" in data else [d.to_dict() for d in suela.detalles]
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error al actualizar la suela", "error": str(e)}), 500
