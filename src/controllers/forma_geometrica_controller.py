from flask import Blueprint, jsonify, request
from models import db, FormaGeometrica

forma_bp = Blueprint("forma_bp", __name__, url_prefix="/formas")


@forma_bp.route("/", methods=["GET"])
def get_all_formas():
    formas = FormaGeometrica.query.all()
    return jsonify([{"id_forma": f.id_forma, "nombre": f.nombre} for f in formas])


@forma_bp.route("/", methods=["POST"])
def create_forma():
    data = request.get_json()
    nombre = data.get("nombre")

    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400

    nueva_forma = FormaGeometrica(nombre=nombre)
    db.session.add(nueva_forma)
    db.session.commit()

    return (
        jsonify({"mensaje": "Forma creada con éxito", "id": nueva_forma.id_forma}),
        201,
    )


@forma_bp.route("/formas/<int:id_forma>", methods=["PATCH"])
def patch_forma(id_forma):
    forma = FormaGeometrica.query.get_or_404(id_forma)
    data = request.get_json()
    nombre = data.get("nombre")

    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400

    forma.nombre = nombre
    db.session.commit()

    return (
        jsonify({"mensaje": "Forma modificada con éxito", "id": forma.id_forma}),
        201,
    )


@forma_bp.route("/formas/<int:id_forma>", methods=["GET"])
def get_forma_by_id(id_forma):
    forma = FormaGeometrica.query.get_or_404(id_forma)
    return jsonify({"id_forma": forma.id_forma, "nombre": forma.nombre})


# Endpoint para actualizar una forma geometrica existente por su ID
@forma_bp.route("/<int:id_forma>", methods=["PUT"])
def update_forma(id_forma):
    try:
        # Busca la forma geometrica por su ID
        forma = FormaGeometrica.query.get(id_forma)

        # Si no se encuentra la forma, devuelve un error 404
        if forma is None:
            return jsonify({"message": "Forma geometrica no encontrada"}), 404

        # Obtener los datos del cuerpo de la peticion (JSON)
        data = request.get_json()

        # Si no se reciben datos JSON, devuelve un error 400
        if not data:
            return (
                jsonify(
                    {"message": "No se recibieron datos JSON para la actualización"}
                ),
                400,
            )

        # Actualiza los campos de la forma con los datos recibidos
        # Solo el nombre por ahora, ya que es el unico campo modificable
        if "nombre" in data:
            # Verificar si el nuevo nombre ya existe
            existing_forma_with_name = FormaGeometrica.query.filter(
                FormaGeometrica.nombre == data["nombre"],
                FormaGeometrica.id_forma != id_forma,
            ).first()
            if existing_forma_with_name:
                return (
                    jsonify(
                        {
                            "message": f"Ya existe otra forma geométrica con el nombre '{data['nombre']}'."
                        }
                    ),
                    409,
                )  # Conflict

            forma.nombre = data["nombre"]
        else:
            return (
                jsonify(
                    {"message": "El campo 'nombre' es requerido para la actualizacion"}
                ),
                400,
            )

        # Confirmar los cambios en la base de datos
        db.session.commit()

        # Devuelve la forma actualizada usando to_dict() y un estado 200 OK
        return (
            jsonify(
                {
                    "message": "Forma geometrica actualizada exitosamente",
                    "forma": forma.to_dict(),
                }
            ),
            200,
        )

    except Exception as e:
        # En caso de error, deshacer la transaccion y devolver un error 500
        db.session.rollback()
        return (
            jsonify(
                {"message": "Error al actualizar la forma geometrica", "error": str(e)}
            ),
            500,
        )
