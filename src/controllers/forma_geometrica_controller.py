from flask import Blueprint, jsonify, request
from models import db, FormaGeometrica, DetalleSuela

forma_bp = Blueprint("forma_bp", __name__, url_prefix="/formas")


@forma_bp.route("/", methods=["GET"])
def get_all_formas():
    formas = FormaGeometrica.query.all()
    return jsonify([forma.to_dict() for forma in formas])


@forma_bp.route("/", methods=["POST"])
def create_forma():
    try:
        data = request.get_json()
        
        if not data or 'nombre' not in data:
            return jsonify({"error": "El nombre de la forma geométrica es requerido"}), 400

        nombre_normalizado = data['nombre'].strip().lower()
        
        forma_existente = FormaGeometrica.query.filter(
            db.func.lower(FormaGeometrica.nombre) == nombre_normalizado
        ).first()
        if forma_existente:
            return jsonify({'error': f'Ya existe una forma geométrica con el nombre "{forma_existente.nombre}"'}), 400

        nueva_forma = FormaGeometrica(nombre=data['nombre'].strip())
        db.session.add(nueva_forma)
        db.session.commit()

        return jsonify({"message": "Forma geométrica creada exitosamente", "forma": nueva_forma.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@forma_bp.route("/<int:id_forma>", methods=["PATCH"])
def update_forma(id_forma):
    try:
        forma = FormaGeometrica.query.get_or_404(id_forma)
        data = request.get_json()
        
        if not data or 'nombre' not in data:
            return jsonify({"error": "El nombre de la forma geométrica es requerido"}), 400

        nombre_normalizado = data['nombre'].strip().lower()
        
        forma_existente = FormaGeometrica.query.filter(
            db.func.lower(FormaGeometrica.nombre) == nombre_normalizado,
            FormaGeometrica.id_forma != id_forma
        ).first()
        if forma_existente:
            return jsonify({'error': f'Ya existe otra forma geométrica con el nombre "{forma_existente.nombre}"'}), 400

        forma.nombre = data['nombre'].strip()
        db.session.commit()

        return jsonify({"message": "Forma geométrica actualizada exitosamente", "forma": forma.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@forma_bp.route("/<int:id_forma>", methods=["GET"])
def get_forma_by_id(id_forma):
    forma = FormaGeometrica.query.get_or_404(id_forma)
    return jsonify(forma.to_dict())


@forma_bp.route("/<int:id_forma>", methods=["DELETE"])
def delete_forma(id_forma):
    try:
        forma = FormaGeometrica.query.get_or_404(id_forma)
        
        detalles = DetalleSuela.query.filter_by(id_forma=id_forma).first()
        if detalles:
            return jsonify({'error': 'No se puede eliminar la forma geométrica porque está siendo utilizada en detalles de suela'}), 400
        
        db.session.delete(forma)
        db.session.commit()
        
        return jsonify({"message": "Forma geométrica eliminada exitosamente"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

    
