from flask import Blueprint, jsonify, request
from models import db, Marca

marca_bp = Blueprint('marca_bp', __name__, url_prefix='/marcas')


@marca_bp.route('/', methods=['GET'])
def get_all_marcas():
    """
    Obtener todas las marcas registradas.
    Este endpoint devuelve una lista de todas las marcas disponibles.
    ---
    tags:
      - Marcas
    responses:
      200:
        description: Lista de marcas.
        schema:
          type: array
          items:
            $ref: '#/definitions/Marca'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    marcas = Marca.query.all()
    return jsonify([marca.to_dict() for marca in marcas])


@marca_bp.route('/<int:id_marca>', methods=['GET'])
def get_marca(id_marca):
    """
    Obtener una marca por su ID.
    Este endpoint devuelve los detalles de una marca específica utilizando su ID.
    ---
    tags:
      - Marcas
    parameters:
      - in: path
        name: id_marca
        type: integer
        required: true
        description: ID único de la marca a obtener.
    responses:
      200:
        description: Detalles de la marca.
        schema:
          $ref: '#/definitions/Marca'
      404:
        description: Marca no encontrada.
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    marca = Marca.query.get_or_404(id_marca)
    return jsonify(marca.to_dict())


@marca_bp.route('/', methods=['POST'])
def create_marca():
    """
    Crear una nueva marca.
    Este endpoint permite crear una nueva marca con un nombre único.
    ---
    tags:
      - Marcas
    parameters:
      - in: body
        name: marca
        description: Objeto de marca a crear.
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              description: Nombre de la nueva marca.
          required:
            - nombre
    responses:
      201:
        description: Marca creada exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
            marca:
              $ref: '#/definitions/Marca'
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
    """
    Actualizar el nombre de una marca existente.
    Este endpoint permite modificar el nombre de una marca específica. El nuevo nombre debe ser único.
    ---
    tags:
      - Marcas
    parameters:
      - in: path
        name: id_marca
        type: integer
        required: true
        description: ID de la marca a actualizar.
      - in: body
        name: marca
        description: Objeto con el nuevo nombre de la marca.
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              description: Nuevo nombre para la marca.
          required:
            - nombre
    responses:
      200:
        description: Marca actualizada exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
            marca:
              $ref: '#/definitions/Marca'
      400:
        description: Error de validación (nombre requerido o duplicado).
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Marca no encontrada.
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
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
    """
    Eliminar una marca por su ID.
    Este endpoint permite eliminar una marca específica, siempre y cuando no esté siendo utilizada por ningún calzado.
    ---
    tags:
      - Marcas
    parameters:
      - in: path
        name: id_marca
        type: integer
        required: true
        description: ID de la marca a eliminar.
    responses:
      200:
        description: Marca eliminada exitosamente.
        schema:
          $ref: '#/definitions/MessageResponse'
      400:
        description: No se puede eliminar la marca porque está asociada a calzados.
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Marca no encontrada.
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
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