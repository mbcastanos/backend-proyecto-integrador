from flask import Blueprint, jsonify, request
from models import db, Calzado, Marca, Modelo, Categoria, Color
from sqlalchemy.orm import joinedload

calzado_bp = Blueprint('calzado_bp', __name__, url_prefix='/calzados')


@calzado_bp.route('/', methods=['GET'])
def get_all_calzados():
    calzados = Calzado.query.options(
        joinedload(Calzado.marca),
        joinedload(Calzado.modelo),
        joinedload(Calzado.categoria),
        joinedload(Calzado.colores)
    ).all()
    resultado = []
    for c in calzados:
        resultado.append(c.to_dict())
    return jsonify(resultado)


@calzado_bp.route('/<int:id_calzado>', methods=['GET'])
def get_calzado(id_calzado):
    calzado = Calzado.query.options(
        joinedload(Calzado.marca),
        joinedload(Calzado.modelo),
        joinedload(Calzado.categoria),
        joinedload(Calzado.colores)
    ).get_or_404(id_calzado)
    return jsonify(calzado.to_dict())


@calzado_bp.route('/', methods=['POST'])
def create_calzado():
    try:
        data = request.get_json()
        
        if 'id_marca' in data and data['id_marca']:
            marca = Marca.query.get(data['id_marca'])
            if not marca:
                return jsonify({'error': 'Marca no encontrada'}), 400
        
        if 'id_modelo' in data and data['id_modelo']:
            modelo = Modelo.query.get(data['id_modelo'])
            if not modelo:
                return jsonify({'error': 'Modelo no encontrado'}), 400
        
        if 'id_categoria' in data and data['id_categoria']:
            categoria = Categoria.query.get(data['id_categoria'])
            if not categoria:
                return jsonify({'error': 'Categoría no encontrada'}), 400

        nuevo_calzado = Calzado(
            alto=data.get('alto'),
            ancho=data.get('ancho'),
            id_marca=data.get('id_marca'),
            id_modelo=data.get('id_modelo'),
            id_categoria=data.get('id_categoria'),
            talle=data.get('talle'),
            tipo_registro=data.get('tipo_registro')
        )
        
        db.session.add(nuevo_calzado)
        db.session.flush()  # Para obtener el ID generado
        
        # Manejar colores si se proporcionan
        if 'id_colores' in data and data['id_colores']:
            for color_id in data['id_colores']:
                color = Color.query.get(color_id)
                if color:
                    nuevo_calzado.colores.append(color)
                else:
                    return jsonify({'error': f'Color con ID {color_id} no encontrado'}), 400
        
        db.session.commit()
        return jsonify({'message': 'Calzado creado exitosamente', 'calzado': nuevo_calzado.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@calzado_bp.route('/getAllDubitadas', methods=['GET'])
def get_all_dubitadas():
    calzados = Calzado.query.options(
        joinedload(Calzado.marca),
        joinedload(Calzado.modelo),
        joinedload(Calzado.categoria),
        joinedload(Calzado.colores)
    ).filter(Calzado.tipo_registro == 'dubitada').all()
    resultado = []
    for c in calzados:
        resultado.append(c.to_dict())
    return jsonify(resultado)


@calzado_bp.route('/getDubitadaById/<int:id_calzado>', methods=['GET'])
def get_dubitada_by_id(id_calzado):
    calzado = Calzado.query.options(
        joinedload(Calzado.marca),
        joinedload(Calzado.modelo),
        joinedload(Calzado.categoria),
        joinedload(Calzado.colores)
    ).get_or_404(id_calzado)
    if calzado.tipo_registro != 'dubitada':
        return jsonify({"error": "Este calzado no es dubitado"}), 400

    return jsonify(calzado.to_dict()), 200


@calzado_bp.route('/getAllIndubitadas', methods=['GET'])
def get_all_indubitadas():
    calzados = Calzado.query.options(
        joinedload(Calzado.marca),
        joinedload(Calzado.modelo),
        joinedload(Calzado.categoria),
        joinedload(Calzado.colores)
    ).filter(Calzado.tipo_registro.in_(['indubitada_proveedor', 'indubitada_comisaria'])).all()
    resultado = []
    for c in calzados:
        resultado.append(c.to_dict())
    return jsonify(resultado)


@calzado_bp.route('/getIndubitadaById/<int:id_calzado>', methods=['GET'])
def get_indubitada_by_id(id_calzado):
    calzado = Calzado.query.options(
        joinedload(Calzado.marca),
        joinedload(Calzado.modelo),
        joinedload(Calzado.categoria),
        joinedload(Calzado.colores)
    ).get_or_404(id_calzado)
    if calzado.tipo_registro not in ['indubitada_proveedor', 'indubitada_comisaria']:
        return jsonify({"error": "Este calzado no es indubitado"}), 400

    return jsonify(calzado.to_dict()), 200


@calzado_bp.route('/<int:id_calzado>', methods=['PATCH'])
def update_calzado(id_calzado):
    try:
        calzado = Calzado.query.get_or_404(id_calzado)
        data = request.get_json()

        if 'alto' in data:
            calzado.alto = data['alto']
        if 'ancho' in data:
            calzado.ancho = data['ancho']
        if 'talle' in data:
            calzado.talle = data['talle']
        if 'tipo_registro' in data:
            calzado.tipo_registro = data['tipo_registro']

        if 'id_marca' in data:
            if data['id_marca']:
                marca = Marca.query.get(data['id_marca'])
                if not marca:
                    return jsonify({'error': 'Marca no encontrada'}), 400
            calzado.id_marca = data['id_marca']

        if 'id_modelo' in data:
            if data['id_modelo']:
                modelo = Modelo.query.get(data['id_modelo'])
                if not modelo:
                    return jsonify({'error': 'Modelo no encontrado'}), 400
            calzado.id_modelo = data['id_modelo']

        if 'id_categoria' in data:
            if data['id_categoria']:
                categoria = Categoria.query.get(data['id_categoria'])
                if not categoria:
                    return jsonify({'error': 'Categoría no encontrada'}), 400
            calzado.id_categoria = data['id_categoria']

        if 'id_colores' in data:
            calzado.colores.clear()
            
            for color_id in data['id_colores']:
                color = Color.query.get(color_id)
                if color:
                    calzado.colores.append(color)
                else:
                    return jsonify({'error': f'Color con ID {color_id} no encontrado'}), 400

        db.session.commit()
        return jsonify({'message': 'Calzado actualizado exitosamente', 'calzado': calzado.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    
@calzado_bp.route('/<int:id_calzado>', methods=['DELETE'])
def delete_calzado(id_calzado):
    try:
        calzado = Calzado.query.get(id_calzado)
        if not calzado:
            return jsonify({'error': f'Calzado con id {id_calzado} no encontrado'}), 404
        
        db.session.delete(calzado)
        db.session.commit()
        return jsonify({'message': f'Calzado con id {id_calzado} eliminado correctamente'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
