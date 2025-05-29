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
