from flask import Blueprint, jsonify, request
from models import db, Color

color_bp = Blueprint('color_bp', __name__, url_prefix='/colores')


@color_bp.route('/', methods=['GET'])
def get_all_colores():
    colores = Color.query.all()
    return jsonify([color.to_dict() for color in colores])


@color_bp.route('/<int:id_color>', methods=['GET'])
def get_color(id_color):
    color = Color.query.get_or_404(id_color)
    return jsonify(color.to_dict())


@color_bp.route('/', methods=['POST'])
def create_color():
    try:
        data = request.get_json()
        
        if not data or 'nombre' not in data:
            return jsonify({'error': 'El nombre del color es requerido'}), 400
        
        nombre_normalizado = data['nombre'].strip().lower()
        
        color_existente = Color.query.filter(
            db.func.lower(Color.nombre) == nombre_normalizado
        ).first()
        if color_existente:
            return jsonify({'error': f'Ya existe un color con el nombre "{color_existente.nombre}"'}), 400
        
        nuevo_color = Color(nombre=data['nombre'].strip())
        db.session.add(nuevo_color)
        db.session.commit()
        
        return jsonify({'message': 'Color creado exitosamente', 'color': nuevo_color.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@color_bp.route('/<int:id_color>', methods=['PATCH'])
def update_color(id_color):
    try:
        color = Color.query.get_or_404(id_color)
        data = request.get_json()
        
        if not data or 'nombre' not in data:
            return jsonify({'error': 'El nombre del color es requerido'}), 400
        
        nombre_normalizado = data['nombre'].strip().lower()
        
        color_existente = Color.query.filter(
            db.func.lower(Color.nombre) == nombre_normalizado,
            Color.id_color != id_color
        ).first()
        if color_existente:
            return jsonify({'error': f'Ya existe otro color con el nombre "{color_existente.nombre}"'}), 400
        
        color.nombre = data['nombre'].strip()
        db.session.commit()
        
        return jsonify({'message': 'Color actualizado exitosamente', 'color': color.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@color_bp.route('/<int:id_color>', methods=['DELETE'])
def delete_color(id_color):
    try:
        color = Color.query.get_or_404(id_color)
        
        if color.calzados:
            return jsonify({'error': 'No se puede eliminar el color porque está siendo utilizado por calzados'}), 400
        
        db.session.delete(color)
        db.session.commit()
        
        return jsonify({'message': 'Color eliminado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400 