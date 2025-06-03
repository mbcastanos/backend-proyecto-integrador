from flask import Blueprint, jsonify, request
from models import db, Calzado

calzado_bp = Blueprint('calzado_bp', __name__, url_prefix='/calzados')


@calzado_bp.route('/', methods=['GET'])
def get_all_calzados():
    calzados = Calzado.query.all()
    resultado = []
    for c in calzados:
        resultado.append({
            'id_calzado': c.id_calzado,
            'categoria': c.categoria,
            'marca': c.marca,
            'modelo': c.modelo,
            'talle': c.talle,
            'ancho': float(c.ancho),
            'alto': float(c.alto),
            'colores': c.colores,
            'tipo_registro': c.tipo_registro
        })
    return jsonify(resultado)


@calzado_bp.route('/<int:id_calzado>', methods=['GET'])
def get_calzado(id_calzado):
    calzado = Calzado.query.get_or_404(id_calzado)
    return jsonify({
        'id_calzado': calzado.id_calzado,
        'categoria': calzado.categoria,
        'marca': calzado.marca,
        'modelo': calzado.modelo,
        'talle': calzado.talle,
        'ancho': float(calzado.ancho),
        'alto': float(calzado.alto),
        'colores': calzado.colores,
        'tipo_registro': calzado.tipo_registro
    })


@calzado_bp.route('/', methods=['POST'])
def create_calzado():
    data = request.get_json()
    nuevo_calzado = Calzado(
        alto=data['alto'],
        ancho=data['ancho'],
        categoria=data['categoria'],
        colores=data['colores'],
        marca=data['marca'],
        modelo=data['modelo'],
        talle=data['talle'],
        tipo_registro=data['tipo_registro']
    )
    db.session.add(nuevo_calzado)
    db.session.commit()
    return jsonify({'message': 'Calzado creado exitosamente'}), 201


@calzado_bp.route('/<int:id_calzado>', methods=['PATCH'])
def update_calzado(id_calzado):
    calzado = Calzado.query.get_or_404(id_calzado)
    data = request.get_json()

    if 'alto' in data:
        calzado.alto = data['alto']
    if 'ancho' in data:
        calzado.ancho = data['ancho']
    if 'categoria' in data:
        calzado.categoria = data['categoria']
    if 'colores' in data:
        calzado.colores = data['colores']
    if 'marca' in data:
        calzado.marca = data['marca']
    if 'modelo' in data:
        calzado.modelo = data['modelo']
    if 'talle' in data:
        calzado.talle = data['talle']
    if 'tipo_registro' in data:
        calzado.tipo_registro = data['tipo_registro']

    db.session.commit()
    return jsonify({'message': 'Calzado actualizado exitosamente'}), 200