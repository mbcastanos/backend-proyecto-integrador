from flask import Blueprint, jsonify, request
from models import db, Categoria

categoria_bp = Blueprint('categoria_bp', __name__, url_prefix='/categorias')


@categoria_bp.route('/', methods=['GET'])
def get_all_categorias():
    categorias = Categoria.query.all()
    return jsonify([categoria.to_dict() for categoria in categorias])


@categoria_bp.route('/<int:id_categoria>', methods=['GET'])
def get_categoria(id_categoria):
    categoria = Categoria.query.get_or_404(id_categoria)
    return jsonify(categoria.to_dict())


@categoria_bp.route('/', methods=['POST'])
def create_categoria():
    try:
        data = request.get_json()
        
        if not data or 'nombre' not in data:
            return jsonify({'error': 'El nombre de la categoría es requerido'}), 400
        
        nombre_normalizado = data['nombre'].strip().lower()
        
        categoria_existente = Categoria.query.filter(
            db.func.lower(Categoria.nombre) == nombre_normalizado
        ).first()
        if categoria_existente:
            return jsonify({'error': f'Ya existe una categoría con el nombre "{categoria_existente.nombre}"'}), 400
        
        nueva_categoria = Categoria(nombre=data['nombre'].strip())
        db.session.add(nueva_categoria)
        db.session.commit()
        
        return jsonify({'message': 'Categoría creada exitosamente', 'categoria': nueva_categoria.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@categoria_bp.route('/<int:id_categoria>', methods=['PATCH'])
def update_categoria(id_categoria):
    try:
        categoria = Categoria.query.get_or_404(id_categoria)
        data = request.get_json()
        
        if not data or 'nombre' not in data:
            return jsonify({'error': 'El nombre de la categoría es requerido'}), 400
        
        nombre_normalizado = data['nombre'].strip().lower()
        
        categoria_existente = Categoria.query.filter(
            db.func.lower(Categoria.nombre) == nombre_normalizado,
            Categoria.id_categoria != id_categoria
        ).first()
        if categoria_existente:
            return jsonify({'error': f'Ya existe otra categoría con el nombre "{categoria_existente.nombre}"'}), 400
        
        categoria.nombre = data['nombre'].strip()
        db.session.commit()
        
        return jsonify({'message': 'Categoría actualizada exitosamente', 'categoria': categoria.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@categoria_bp.route('/<int:id_categoria>', methods=['DELETE'])
def delete_categoria(id_categoria):
    try:
        categoria = Categoria.query.get_or_404(id_categoria)
        
        if categoria.calzados:
            return jsonify({'error': 'No se puede eliminar la categoría porque está siendo utilizada por calzados'}), 400
        
        db.session.delete(categoria)
        db.session.commit()
        
        return jsonify({'message': 'Categoría eliminada exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400 