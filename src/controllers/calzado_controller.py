from flask import Blueprint, jsonify, request
from models import db, Calzado, Marca, Modelo, Categoria, Color
from models import Imputado
from models import CalzadoImputado
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
    

@calzado_bp.route('/cargar_calzado_imputado', methods=['POST'])
def cargar_calzado_imputado():
    try:
        data = request.get_json()
        

        if not data or 'imputado' not in data or 'calzado' not in data:
            return jsonify({'error': 'Datos incompletos'}), 400
        

        imputado_data = data['imputado']
        nuevo_imputado = Imputado(
            nombre=imputado_data.get('nombre'),
            dni=imputado_data.get('dni'),
            direccion=imputado_data.get('direccion'),
            comisaria=imputado_data.get('comisaria'),
            jurisdiccion=imputado_data.get('jurisdiccion')
        )
        db.session.add(nuevo_imputado)
        db.session.flush()  
        

        calzado_data = data['calzado']
        nuevo_calzado = Calzado(
            talle=calzado_data.get('talle'),
            ancho=calzado_data.get('ancho'),
            alto=calzado_data.get('alto'),
            tipo_registro=calzado_data.get('tipo_registro'),
            id_marca=calzado_data.get('id_marca'),
            id_modelo=calzado_data.get('id_modelo'),
            id_categoria=calzado_data.get('id_categoria')
        )
        db.session.add(nuevo_calzado)
        db.session.flush()
        

        relacion = CalzadoImputado(
            calzado_id_calzado=nuevo_calzado.id_calzado,
            imputado_id=nuevo_imputado.id
        )
        db.session.add(relacion)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Datos cargados exitosamente',
            'imputado_id': nuevo_imputado.id,
            'calzado_id': nuevo_calzado.id_calzado
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@calzado_bp.route('/buscar_por_dni/<dni>', methods=['GET'])
def buscar_calzados_por_dni(dni):
    try:

        imputado = Imputado.query.filter_by(dni=dni).first()
        
        if not imputado:
            return jsonify({'error': f'No se encontró imputado con DNI: {dni}'}), 404

        calzados_imputado = CalzadoImputado.query.filter_by(
            imputado_id=imputado.id
        ).all()
        
        calzados_data = []
        for relacion in calzados_imputado:
            calzado = Calzado.query.options(
                joinedload(Calzado.marca),
                joinedload(Calzado.modelo),
                joinedload(Calzado.categoria),
                joinedload(Calzado.colores)
            ).get(relacion.calzado_id_calzado)
            
            if calzado:
                calzados_data.append(calzado.to_dict())
        
        resultado = {
            'imputado': imputado.to_dict(),
            'calzados': calzados_data
        }
        
        return jsonify(resultado), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@calzado_bp.route('/todos_imputados_con_calzados', methods=['GET'])
def get_todos_imputados_con_calzados():
    try:

        imputados = Imputado.query.all()
        
        resultado = []
        
        for imputado in imputados:
            calzados_imputado = CalzadoImputado.query.filter_by(
                imputado_id=imputado.id
            ).all()
            
            calzados_data = []
            for relacion in calzados_imputado:
                calzado = Calzado.query.options(
                    joinedload(Calzado.marca),
                    joinedload(Calzado.modelo),
                    joinedload(Calzado.categoria),
                    joinedload(Calzado.colores)
                ).get(relacion.calzado_id_calzado)
                
                if calzado:
                    calzados_data.append(calzado.to_dict())
            
            resultado.append({
                'imputado': imputado.to_dict(),
                'calzados': calzados_data
            })
        
        return jsonify(resultado), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@calzado_bp.route('/editar_calzado_imputado/<int:id_calzado>', methods=['PATCH'])
def editar_calzado_e_imputado(id_calzado):
    data = request.get_json()
    calzado_data = data.get("calzado")
    imputado_data = data.get("imputado")

    calzado = Calzado.query.get(id_calzado)
    if not calzado:
        return jsonify({"error": "Calzado no encontrado"}), 404

    imputado = (
        CalzadoImputado.query
        .filter_by(calzado_id_calzado=id_calzado)
        .first()
    )
    if not imputado:
        return jsonify({"error": "Imputado no asociado a este calzado"}), 404

    for key, value in calzado_data.items():
        setattr(calzado, key, value)

    for key, value in imputado_data.items():
        setattr(imputado, key, value)

    db.session.commit()
    return jsonify({"message": "Actualizado correctamente"}), 200


@calzado_bp.route('/asignar_calzado_imputado', methods=['POST'])
def asignar_calzado_imputado():
    data = request.get_json()
    id_calzado = data.get("id_calzado")
    id_imputado = data.get("id_imputado")

    nueva_relacion = CalzadoImputado(
        calzado_id_calzado=id_calzado,
        imputado_id_imputado=id_imputado
    )
    db.session.add(nueva_relacion)
    db.session.commit()

    return jsonify({"message": "Asignación realizada correctamente"}), 201

@calzado_bp.route('/eliminar_calzado_imputado', methods=['DELETE'])
def eliminar_relacion_calzado_imputado():
    data = request.get_json()
    dni = data["imputado"]["dni"]
    calzado_id = data["calzado_id"]

    relacion = (
        CalzadoImputado.query
        .join(Imputado)
        .filter(Imputado.dni == dni, CalzadoImputado.calzado_id_calzado == calzado_id)
        .first()
    )

    if not relacion:
        return jsonify({"error": "Relación no encontrada"}), 404

    db.session.delete(relacion)
    db.session.commit()

    return jsonify({"message": "Relación eliminada correctamente"}), 200
