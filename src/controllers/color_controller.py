from flask import Blueprint, jsonify, request
from models import db, Color

color_bp = Blueprint('color_bp', __name__, url_prefix='/colores')


@color_bp.route('/', methods=['GET'])
def get_all_colores():
    """
    Obtener todos los colores registrados.
    Este endpoint devuelve una lista de todos los colores disponibles.
    ---
    tags:
      - Colores
    responses:
      200:
        description: Lista de colores.
        schema:
          type: array
          items:
            $ref: '#/definitions/Color'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    colores = Color.query.all()
    return jsonify([color.to_dict() for color in colores])


@color_bp.route('/<int:id_color>', methods=['GET'])
def get_color(id_color):
    """
    Obtener un color por su ID.
    Este endpoint devuelve los detalles de un color específico utilizando su ID.
    ---
    tags:
      - Colores
    parameters:
      - in: path
        name: id_color
        type: integer
        required: true
        description: ID único del color a obtener.
    responses:
      200:
        description: Detalles del color.
        schema:
          $ref: '#/definitions/Color'
      404:
        description: Color no encontrado.
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    color = Color.query.get_or_404(id_color)
    return jsonify(color.to_dict())


@color_bp.route('/', methods=['POST'])
def create_color():
    """
    Crear un nuevo color.
    Este endpoint permite crear un nuevo color con un nombre único.
    ---
    tags:
      - Colores
    parameters:
      - in: body
        name: color
        description: Objeto de color a crear.
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              description: Nombre del nuevo color.
          required:
            - nombre
    responses:
      201:
        description: Color creado exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
            color:
              $ref: '#/definitions/Color'
      400:
        description: Error de validación (nombre requerido o duplicado).
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
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
    """
    Actualizar el nombre de un color existente.
    Este endpoint permite modificar el nombre de un color específico. El nuevo nombre debe ser único.
    ---
    tags:
      - Colores
    parameters:
      - in: path
        name: id_color
        type: integer
        required: true
        description: ID del color a actualizar.
      - in: body
        name: color
        description: Objeto con el nuevo nombre del color.
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              description: Nuevo nombre para el color.
          required:
            - nombre
    responses:
      200:
        description: Color actualizado exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
            color:
              $ref: '#/definitions/Color'
      400:
        description: Error de validación (nombre requerido o duplicado).
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Color no encontrado.
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
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
    """
    Eliminar un color por su ID.
    Este endpoint permite eliminar un color específico, siempre y cuando no esté siendo utilizado por ningún calzado.
    ---
    tags:
      - Colores
    parameters:
      - in: path
        name: id_color
        type: integer
        required: true
        description: ID del color a eliminar.
    responses:
      200:
        description: Color eliminado exitosamente.
        schema:
          $ref: '#/definitions/MessageResponse'
      400:
        description: No se puede eliminar el color porque está asociado a calzados.
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Color no encontrado.
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
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