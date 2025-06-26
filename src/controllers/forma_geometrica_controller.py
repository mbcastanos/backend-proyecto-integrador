from flask import Blueprint, jsonify, request
from models import db, FormaGeometrica, DetalleSuela

forma_bp = Blueprint("forma_bp", __name__, url_prefix="/formas")


@forma_bp.route("/", methods=["GET"])
def get_all_formas():
    """
    Obtener todas las formas geométricas registradas.
    Este endpoint devuelve una lista de todas las formas geométricas disponibles.
    ---
    tags:
      - Formas Geométricas
    responses:
      200:
        description: Lista de formas geométricas.
        schema:
          type: array
          items:
            $ref: '#/definitions/FormaGeometrica'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    formas = FormaGeometrica.query.all()
    return jsonify([forma.to_dict() for forma in formas])


@forma_bp.route("/", methods=["POST"])
def create_forma():
    """
    Crear una nueva forma geométrica.
    Este endpoint permite crear una nueva forma geométrica con un nombre único.
    ---
    tags:
      - Formas Geométricas
    parameters:
      - in: body
        name: forma
        description: Objeto de forma geométrica a crear.
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              description: Nombre de la nueva forma geométrica.
          required:
            - nombre
    responses:
      201:
        description: Forma geométrica creada exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
            forma:
              $ref: '#/definitions/FormaGeometrica'
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
            return jsonify({"error": "El nombre de la forma geométrica es requerido"}), 400

        nombre_normalizado = data['nombre'].strip().lower()
        
        forma_existente = FormaGeometrica.query.filter(
            db.func.lower(FormaGeometrica.nombre) == nombre_normalizado
        ).first()
        if forma_existente:
            return jsonify({'error': f'Ya existe una forma geométrica con el nombre "{forma_existente.nombre}"'}), 400

        nueva_forma = FormaGeometrica(nombre=data['nombre'].strip())
        db.session.add(nueva_forma)
        db.session.commit()

        return jsonify({"message": "Forma geométrica creada exitosamente", "forma": nueva_forma.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@forma_bp.route("/<int:id_forma>", methods=["PATCH"])
def update_forma(id_forma):
    """
    Actualizar el nombre de una forma geométrica existente.
    Este endpoint permite modificar el nombre de una forma geométrica específica. El nuevo nombre debe ser único.
    ---
    tags:
      - Formas Geométricas
    parameters:
      - in: path
        name: id_forma
        type: integer
        required: true
        description: ID de la forma geométrica a actualizar.
      - in: body
        name: forma
        description: Objeto con el nuevo nombre de la forma geométrica.
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              description: Nuevo nombre para la forma geométrica.
          required:
            - nombre
    responses:
      200:
        description: Forma geométrica actualizada exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
            forma:
              $ref: '#/definitions/FormaGeometrica'
      400:
        description: Error de validación (nombre requerido o duplicado).
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Forma geométrica no encontrada.
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    try:
        forma = FormaGeometrica.query.get_or_404(id_forma)
        data = request.get_json()
        
        if not data or 'nombre' not in data:
            return jsonify({"error": "El nombre de la forma geométrica es requerido"}), 400

        nombre_normalizado = data['nombre'].strip().lower()
        
        forma_existente = FormaGeometrica.query.filter(
            db.func.lower(FormaGeometrica.nombre) == nombre_normalizado,
            FormaGeometrica.id_forma != id_forma
        ).first()
        if forma_existente:
            return jsonify({'error': f'Ya existe otra forma geométrica con el nombre "{forma_existente.nombre}"'}), 400

        forma.nombre = data['nombre'].strip()
        db.session.commit()

        return jsonify({"message": "Forma geométrica actualizada exitosamente", "forma": forma.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@forma_bp.route("/<int:id_forma>", methods=["GET"])
def get_forma_by_id(id_forma):
    """
    Obtener una forma geométrica por su ID.
    Este endpoint devuelve los detalles de una forma geométrica específica utilizando su ID.
    ---
    tags:
      - Formas Geométricas
    parameters:
      - in: path
        name: id_forma
        type: integer
        required: true
        description: ID único de la forma geométrica a obtener.
    responses:
      200:
        description: Detalles de la forma geométrica.
        schema:
          $ref: '#/definitions/FormaGeometrica'
      404:
        description: Forma geométrica no encontrada.
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    forma = FormaGeometrica.query.get_or_404(id_forma)
    return jsonify(forma.to_dict())


@forma_bp.route("/<int:id_forma>", methods=["DELETE"])
def delete_forma(id_forma):
    """
    Eliminar una forma geométrica por su ID.
    Este endpoint permite eliminar una forma geométrica específica, siempre y cuando no esté siendo utilizada en ningún detalle de suela.
    ---
    tags:
      - Formas Geométricas
    parameters:
      - in: path
        name: id_forma
        type: integer
        required: true
        description: ID de la forma geométrica a eliminar.
    responses:
      200:
        description: Forma geométrica eliminada exitosamente.
        schema:
          $ref: '#/definitions/MessageResponse'
      400:
        description: No se puede eliminar la forma geométrica porque está asociada a detalles de suela.
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Forma geométrica no encontrada.
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    try:
        forma = FormaGeometrica.query.get_or_404(id_forma)
        
        detalles = DetalleSuela.query.filter_by(id_forma=id_forma).first()
        if detalles:
            return jsonify({'error': 'No se puede eliminar la forma geométrica porque está siendo utilizada en detalles de suela'}), 400
        
        db.session.delete(forma)
        db.session.commit()
        
        return jsonify({"message": "Forma geométrica eliminada exitosamente"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

    
