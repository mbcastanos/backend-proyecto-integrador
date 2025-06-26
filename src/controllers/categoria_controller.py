from flask import Blueprint, jsonify, request
from models import db, Categoria

categoria_bp = Blueprint('categoria_bp', __name__, url_prefix='/categorias')


@categoria_bp.route('/', methods=['GET'])
def get_all_categorias():
    """
    Obtener todas las categorías registradas.
    Este endpoint devuelve una lista de todas las categorías disponibles.
    ---
    tags:
      - Categorías
    responses:
      200:
        description: Lista de categorías.
        schema:
          type: array
          items:
            $ref: '#/definitions/Categoria'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    categorias = Categoria.query.all()
    return jsonify([categoria.to_dict() for categoria in categorias])


@categoria_bp.route('/<int:id_categoria>', methods=['GET'])
def get_categoria(id_categoria):
    """
    Obtener una categoría por su ID.
    Este endpoint devuelve los detalles de una categoría específica utilizando su ID.
    ---
    tags:
      - Categorías
    parameters:
      - in: path
        name: id_categoria
        type: integer
        required: true
        description: ID único de la categoría a obtener.
    responses:
      200:
        description: Detalles de la categoría.
        schema:
          $ref: '#/definitions/Categoria'
      404:
        description: Categoría no encontrada.
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    categoria = Categoria.query.get_or_404(id_categoria)
    return jsonify(categoria.to_dict())


@categoria_bp.route('/', methods=['POST'])
def create_categoria():
    """
    Crear una nueva categoría.
    Este endpoint permite crear una nueva categoría con un nombre único.
    ---
    tags:
      - Categorías
    parameters:
      - in: body
        name: categoria
        description: Objeto de categoría a crear.
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              description: Nombre de la nueva categoría.
          required:
            - nombre
    responses:
      201:
        description: Categoría creada exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
            categoria:
              $ref: '#/definitions/Categoria'
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
    """
    Actualizar el nombre de una categoría existente.
    Este endpoint permite modificar el nombre de una categoría específica. El nuevo nombre debe ser único.
    ---
    tags:
      - Categorías
    parameters:
      - in: path
        name: id_categoria
        type: integer
        required: true
        description: ID de la categoría a actualizar.
      - in: body
        name: categoria
        description: Objeto con el nuevo nombre de la categoría.
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              description: Nuevo nombre para la categoría.
          required:
            - nombre
    responses:
      200:
        description: Categoría actualizada exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
            categoria:
              $ref: '#/definitions/Categoria'
      400:
        description: Error de validación (nombre requerido o duplicado).
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Categoría no encontrada.
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
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
    """
    Eliminar una categoría por su ID.
    Este endpoint permite eliminar una categoría específica, siempre y cuando no esté siendo utilizada por ningún calzado.
    ---
    tags:
      - Categorías
    parameters:
      - in: path
        name: id_categoria
        type: integer
        required: true
        description: ID de la categoría a eliminar.
    responses:
      200:
        description: Categoría eliminada exitosamente.
        schema:
          $ref: '#/definitions/MessageResponse'
      400:
        description: No se puede eliminar la categoría porque está asociada a calzados.
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Categoría no encontrada.
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
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