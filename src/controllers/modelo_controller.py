from flask import Blueprint, jsonify, request
from models import db, Modelo

modelo_bp = Blueprint('modelo_bp', __name__, url_prefix='/modelos')


@modelo_bp.route('/', methods=['GET'])
def get_all_modelos():
    modelos = Modelo.query.all()
    return jsonify([modelo.to_dict() for modelo in modelos])


@modelo_bp.route('/<int:id_modelo>', methods=['GET'])
def get_modelo(id_modelo):
    modelo = Modelo.query.get_or_404(id_modelo)
    return jsonify(modelo.to_dict())


@modelo_bp.route('/', methods=['POST'])
def create_modelo():
    try:
        data = request.get_json()
        
        if not data or 'nombre' not in data:
            return jsonify({'error': 'El nombre del modelo es requerido'}), 400
        
        nombre_normalizado = data['nombre'].strip().lower()
        
        modelo_existente = Modelo.query.filter(
            db.func.lower(Modelo.nombre) == nombre_normalizado
        ).first()
        if modelo_existente:
            return jsonify({'error': f'Ya existe un modelo con el nombre "{modelo_existente.nombre}"'}), 400
        
        nuevo_modelo = Modelo(nombre=data['nombre'].strip())
        db.session.add(nuevo_modelo)
        db.session.commit()
        
        return jsonify({'message': 'Modelo creado exitosamente', 'modelo': nuevo_modelo.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@modelo_bp.route('/<int:id_modelo>', methods=['PATCH'])
def update_modelo(id_modelo):
    try:
        modelo = Modelo.query.get_or_404(id_modelo)
        data = request.get_json()
        
        if not data or 'nombre' not in data:
            return jsonify({'error': 'El nombre del modelo es requerido'}), 400
        
        nombre_normalizado = data['nombre'].strip().lower()
        
        modelo_existente = Modelo.query.filter(
            db.func.lower(Modelo.nombre) == nombre_normalizado,
            Modelo.id_modelo != id_modelo
        ).first()
        if modelo_existente:
            return jsonify({'error': f'Ya existe otro modelo con el nombre "{modelo_existente.nombre}"'}), 400
        
        modelo.nombre = data['nombre'].strip()
        db.session.commit()
        
        return jsonify({'message': 'Modelo actualizado exitosamente', 'modelo': modelo.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@modelo_bp.route('/<int:id_modelo>', methods=['DELETE'])
def delete_modelo(id_modelo):
    try:
        modelo = Modelo.query.get_or_404(id_modelo)
        
        if modelo.calzados:
            return jsonify({'error': 'No se puede eliminar el modelo porque está siendo utilizado por calzados'}), 400
        
        db.session.delete(modelo)
        db.session.commit()
        
        return jsonify({'message': 'Modelo eliminado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400 