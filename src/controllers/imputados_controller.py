from flask import Blueprint, jsonify, request
from models import db, Imputado
from models import db, Imputado, Calzado


imputados_bp = Blueprint('imputados_bp', __name__, url_prefix='/imputados')

@imputados_bp.route('/', methods=['GET'])
def get_all_imputados():
    imputados = Imputado.query.all()
    return jsonify([imputado.to_dict() for imputado in imputados])

@imputados_bp.route('/<int:id_imputado>', methods=['GET'])
def get_imputado(id_imputado):
    imputado = Imputado.query.get_or_404(id_imputado)
    return jsonify(imputado.to_dict())

@imputados_bp.route('/', methods=['POST'])
def create_imputado():
    try:
        data = request.get_json()

        campos_obligatorios = ['nombre', 'dni', 'direccion', 'comisaria', 'jurisdiccion']
        campos_faltantes = [campo for campo in campos_obligatorios if not data or campo not in data or not data[campo]]
        
        if campos_faltantes:
            return jsonify({
                'error': f'Los siguientes campos son obligatorios: {", ".join(campos_faltantes)}'
            }), 400
        
        nombre_normalizado = data['nombre'].strip().lower()
        
        imputado_existente = Imputado.query.filter(
            db.func.lower(Imputado.nombre) == nombre_normalizado
        ).first()
        if imputado_existente:
            return jsonify({'error': f'Ya existe un imputado con el nombre "{imputado_existente.nombre}"'}), 400
        
        nuevo_imputado = Imputado(
            nombre=nombre_normalizado,
            dni=data['dni'],    
            direccion=data['direccion'],
            comisaria=data['comisaria'],
            jurisdiccion=data['jurisdiccion']
        )
        db.session.add(nuevo_imputado)
        db.session.commit()
        return jsonify(nuevo_imputado.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@imputados_bp.route('/<int:id_imputado>', methods=['PATCH'])
def update_imputado(id_imputado):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Se requiere al menos un campo para actualizar'}), 400
        
        imputado = Imputado.query.get_or_404(id_imputado)
        
        if 'nombre' in data:
            if not data['nombre']:
                return jsonify({'error': 'El nombre no puede estar vacío'}), 400
            
            nombre_normalizado = data['nombre'].strip().lower()
            imputado_existente = Imputado.query.filter(
                db.func.lower(Imputado.nombre) == nombre_normalizado,
                Imputado.id != id_imputado 
            ).first()
            if imputado_existente:
                return jsonify({'error': f'Ya existe un imputado con el nombre "{imputado_existente.nombre}"'}), 400
            
            imputado.nombre = data['nombre']
        
        if 'dni' in data:
            imputado.dni = data['dni']
        if 'direccion' in data:
            imputado.direccion = data['direccion']
        if 'comisaria' in data:
            imputado.comisaria = data['comisaria']
        if 'jurisdiccion' in data:
            imputado.jurisdiccion = data['jurisdiccion']
        
        db.session.commit()
        return jsonify(imputado.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

@imputados_bp.route('/<int:id_imputado>', methods=['DELETE'])
def delete_imputado(id_imputado):
    try:
        imputado = Imputado.query.get_or_404(id_imputado)
        
        if imputado.calzados:
            return jsonify({'error': 'No se puede eliminar el imputado porque tiene calzados asociados'}), 409
        
        db.session.delete(imputado)
        db.session.commit()
        return jsonify({'message': 'Imputado eliminado correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


    
    
@imputados_bp.route('/<int:id_imputado>/calzados/<int:id_calzado>', methods=['PATCH'])
def editar_calzado_relacionado(id_imputado, id_calzado):
    imputado = Imputado.query.get_or_404(id_imputado)
    calzado = Calzado.query.get_or_404(id_calzado)

    if calzado not in imputado.calzados:
        return jsonify({'error': 'El calzado no está vinculado a este imputado'}), 404

    data = request.get_json()
    if 'talle' in data:
        calzado.talle = data['talle']
    if 'ancho' in data:
        calzado.ancho = data['ancho']
    if 'alto' in data:
        calzado.alto = data['alto']
    if 'tipo_registro' in data:
        calzado.tipo_registro = data['tipo_registro']

    db.session.commit()
    return jsonify({'message': 'Calzado editado correctamente', 'calzado': calzado.to_dict()})


@imputados_bp.route('/<int:id_imputado>/calzados/<int:id_calzado>', methods=['POST'])
def asociar_calzado_a_imputado(id_imputado, id_calzado):
    imputado = Imputado.query.get_or_404(id_imputado)
    calzado = Calzado.query.get_or_404(id_calzado)

    if calzado in imputado.calzados:
        return jsonify({'error': 'El calzado ya está vinculado a este imputado'}), 400

    imputado.calzados.append(calzado)
    db.session.commit()

    return jsonify({'message': 'Calzado vinculado correctamente al imputado'}), 201



@imputados_bp.route('/<int:id_imputado>/calzados/<int:id_calzado>', methods=['DELETE'])
def eliminar_calzado_de_imputado(id_imputado, id_calzado):
    imputado = Imputado.query.get_or_404(id_imputado)
    calzado = Calzado.query.get_or_404(id_calzado)

    if calzado not in imputado.calzados:
        return jsonify({'error': 'El calzado no está vinculado a este imputado'}), 404

    imputado.calzados.remove(calzado)

   
    if not calzado.imputados:
        db.session.delete(calzado)

    db.session.commit()
    return jsonify({'message': 'Calzado desvinculado correctamente del imputado'}), 200
