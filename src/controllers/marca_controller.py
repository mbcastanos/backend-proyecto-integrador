from flask import Blueprint, jsonify, request
from models import db, Marca

marca_bp = Blueprint('marca_bp', __name__, url_prefix='/marcas')


@marca_bp.route('/', methods=['GET'])
def get_all_marcas():
    marcas = Marca.query.all()
    return jsonify([marca.to_dict() for marca in marcas])


@marca_bp.route('/<int:id_marca>', methods=['GET'])
def get_marca(id_marca):
    marca = Marca.query.get_or_404(id_marca)
    return jsonify(marca.to_dict())


@marca_bp.route('/', methods=['POST'])
def create_marca():
    try:
        data = request.get_json()
        
        if not data or 'nombre' not in data:
            return jsonify({'error': 'El nombre de la marca es requerido'}), 400        

        nombre_normalizado = data['nombre'].strip().lower()
        
        marca_existente = Marca.query.filter(
            db.func.lower(Marca.nombre) == nombre_normalizado
        ).first()
        if marca_existente:
            return jsonify({'error': f'Ya existe una marca con el nombre "{marca_existente.nombre}"'}), 400

        nueva_marca = Marca(nombre=data['nombre'].strip())
        db.session.add(nueva_marca)
        db.session.commit()
        
        return jsonify({'message': 'Marca creada exitosamente', 'marca': nueva_marca.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@marca_bp.route('/<int:id_marca>', methods=['PATCH'])
def update_marca(id_marca):
    try:
        marca = Marca.query.get_or_404(id_marca)
        data = request.get_json()
        
        if not data or 'nombre' not in data:
            return jsonify({'error': 'El nombre de la marca es requerido'}), 400
        
        nombre_normalizado = data['nombre'].strip().lower()
        
        marca_existente = Marca.query.filter(
            db.func.lower(Marca.nombre) == nombre_normalizado,
            Marca.id_marca != id_marca
        ).first()
        if marca_existente:
            return jsonify({'error': f'Ya existe otra marca con el nombre "{marca_existente.nombre}"'}), 400
        
        marca.nombre = data['nombre'].strip()
        db.session.commit()
        
        return jsonify({'message': 'Marca actualizada exitosamente', 'marca': marca.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@marca_bp.route('/<int:id_marca>', methods=['DELETE'])
def delete_marca(id_marca):
    try:
        marca = Marca.query.get_or_404(id_marca)
        
        if marca.calzados:
            return jsonify({'error': 'No se puede eliminar la marca porque está siendo utilizada por calzados'}), 400
        
        db.session.delete(marca)
        db.session.commit()
        
        return jsonify({'message': 'Marca eliminada exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400 