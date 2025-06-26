from flask import Blueprint, jsonify, request
from models import db, Modelo

modelo_bp = Blueprint('modelo_bp', __name__, url_prefix='/modelos')


@modelo_bp.route('/', methods=['GET'])
def get_all_modelos():
    """
    Obtener todos los modelos registrados.
    Este endpoint devuelve una lista de todos los modelos disponibles.
    ---
    tags:
      - Modelos
    responses:
      200:
        description: Lista de modelos.
        schema:
          type: array
          items:
            $ref: '#/definitions/Modelo'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    modelos = Modelo.query.all()
    return jsonify([modelo.to_dict() for modelo in modelos])


@modelo_bp.route('/<int:id_modelo>', methods=['GET'])
def get_modelo(id_modelo):
    """
    Obtener un modelo por su ID.
    Este endpoint devuelve los detalles de un modelo específico utilizando su ID.
    ---
    tags:
      - Modelos
    parameters:
      - in: path
        name: id_modelo
        type: integer
        required: true
        description: ID único del modelo a obtener.
    responses:
      200:
        description: Detalles del modelo.
        schema:
          $ref: '#/definitions/Modelo'
      404:
        description: Modelo no encontrado.
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    modelo = Modelo.query.get_or_404(id_modelo)
    return jsonify(modelo.to_dict())


@modelo_bp.route('/', methods=['POST'])
def create_modelo():
    """
    Crear un nuevo modelo.
    Este endpoint permite crear un nuevo modelo con un nombre único.
    ---
    tags:
      - Modelos
    parameters:
      - in: body
        name: modelo
        description: Objeto de modelo a crear.
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              description: Nombre del nuevo modelo.
          required:
            - nombre
    responses:
      201:
        description: Modelo creado exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
            modelo:
              $ref: '#/definitions/Modelo'
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
    """
    Actualizar el nombre de un modelo existente.
    Este endpoint permite modificar el nombre de un modelo específico. El nuevo nombre debe ser único.
    ---
    tags:
      - Modelos
    parameters:
      - in: path
        name: id_modelo
        type: integer
        required: true
        description: ID del modelo a actualizar.
      - in: body
        name: modelo
        description: Objeto con el nuevo nombre del modelo.
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              description: Nuevo nombre para el modelo.
          required:
            - nombre
    responses:
      200:
        description: Modelo actualizado exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
            modelo:
              $ref: '#/definitions/Modelo'
      400:
        description: Error de validación (nombre requerido o duplicado).
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Modelo no encontrado.
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
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
    """
    Eliminar un modelo por su ID.
    Este endpoint permite eliminar un modelo específico, siempre y cuando no esté siendo utilizado por ningún calzado.
    ---
    tags:
      - Modelos
    parameters:
      - in: path
        name: id_modelo
        type: integer
        required: true
        description: ID del modelo a eliminar.
    responses:
      200:
        description: Modelo eliminado exitosamente.
        schema:
          $ref: '#/definitions/MessageResponse'
      400:
        description: No se puede eliminar el modelo porque está asociado a calzados.
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Modelo no encontrado.
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
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