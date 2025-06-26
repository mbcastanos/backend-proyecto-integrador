import datetime
import jwt
import bcrypt
from flask import Blueprint, Response, g, json, jsonify, request
from models import db, Usuario
from controllers.auth import token_required
from dotenv import load_dotenv
import os

load_dotenv()
# Para los que hagan pull: definan esta variable de entorno en un archivo .env
# Esto es temporal hasta que se suba el codigo a un servidor
secret_key = os.getenv("SECRET_KEY")

login_bp = Blueprint('login_bp', __name__)


@login_bp.route("/auth/login", methods = ["POST"])
def login():
    """
    Iniciar sesión de usuario.
    Este endpoint permite a un usuario autenticarse con su nombre de usuario y contraseña, y si las credenciales son correctas, devuelve un token JWT.
    ---
    tags:
      - Autenticación
    parameters:
      - in: body
        name: credenciales
        description: Credenciales del usuario para iniciar sesión.
        required: true
        schema:
          $ref: '#/definitions/LoginInput'
    responses:
      200:
        description: Inicio de sesión exitoso.
        schema:
          $ref: '#/definitions/LoginResponse'
      400:
        description: Usuario y/o contraseña obligatorios.
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: Credenciales incorrectas.
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "el usuario y la contraseña son obligatorios"}), 400
    
    usuario = Usuario.query.filter_by(username=username).first()
    
    if not usuario or not bcrypt.checkpw(password.encode(), usuario.password_hash.encode()):
        return jsonify({"error": "Credenciales incorrectas"}), 401
    
    payload = {
        "user_id": usuario.id,
        "username": usuario.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # token válido 1 hora
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")

    return jsonify({"message" : "inicio valido", "token" : token}), 200
    
@login_bp.route("/usuarios", methods = ["POST"])
@token_required
def create_user():
    """
    Crear un nuevo usuario (requiere token de autenticación).
    Este endpoint permite a un administrador (o usuario con rol adecuado) crear un nuevo usuario con un nombre de usuario, contraseña y rol.
    ---
    tags:
      - Usuarios
    security:
      - JWT: []
    parameters:
      - in: body
        name: usuario
        description: Objeto del usuario a crear.
        required: true
        schema:
          $ref: '#/definitions/UsuarioInput'
    responses:
      201:
        description: Usuario creado exitosamente.
        schema:
          $ref: '#/definitions/MessageResponse'
      400:
        description: Campos obligatorios faltantes o usuario ya existente.
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: No autorizado (token faltante o inválido).
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")
    if not username or not password or not role:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400
    
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    if Usuario.query.filter_by(username=username).first():
        return jsonify({"error": "El usuario ya existe"}), 400

    nuevo_usuario = Usuario(
        username=username,
        password_hash=password_hash.decode('utf-8'),  # guardamos como string
        role=role
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"msg": "Usuario creado exitosamente."}), 201

@login_bp.route("/me", methods=["GET"])
@token_required
def obtener_usuario_actual():
    """
    Obtener información del usuario autenticado (requiere token de autenticación).
    Este endpoint devuelve los detalles del usuario cuya sesión está activa, basándose en el token JWT proporcionado.
    ---
    tags:
      - Usuarios
    security:
      - JWT: []
    responses:
      200:
        description: Información del usuario actual.
        schema:
          $ref: '#/definitions/Usuario'
      401:
        description: No autorizado (token faltante o inválido).
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Usuario no encontrado (raro si el token es válido).
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    usuario = Usuario.query.get(g.user["user_id"])
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({
        "id": usuario.id,
        "username": usuario.username,
        "role": usuario.role
    }), 200

@login_bp.route("/usuarios/<int:user_id>", methods=["PATCH"])
@token_required
def actualizar_usuario(user_id):
    """
    Actualizar un usuario por su ID (requiere token de autenticación).
    Este endpoint permite modificar el nombre de usuario, contraseña y/o rol de un usuario existente.
    ---
    tags:
      - Usuarios
    security:
      - JWT: []
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        description: ID del usuario a actualizar.
      - in: body
        name: usuario
        description: Objeto con los campos del usuario a actualizar.
        required: true
        schema:
          $ref: '#/definitions/UsuarioInput'
    responses:
      200:
        description: Usuario actualizado exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
            new_token:
              type: string
      400:
        description: Nombre de usuario ya en uso o no se proporcionaron datos para actualizar.
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: No autorizado (token faltante o inválido).
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Usuario no encontrado.
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    data = request.get_json()
    
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({"error" : "Usuario no encontrado" }), 404
    
    new_username = data.get("username")
    new_password = data.get("password")
    new_role = data.get("role")

    if new_username:
        if Usuario.query.filter(Usuario.username==new_username, Usuario.id != user_id).first():
            return jsonify({"error": "El nombre de usuario ya está en uso"}), 400
        usuario.username = new_username
    
    if new_password:
        usuario.password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode('utf-8')
    
    if new_role:
        usuario.role = new_role


    if not new_username and not new_password and not new_role:
        return jsonify({"error": "No se dieron datos para actualizar"}), 400

    db.session.commit()

    new_payload = {
        "user_id": usuario.id,
        "username": usuario.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # token válido 1 hora
    }

    new_token = jwt.encode(new_payload, secret_key, algorithm="HS256")

    return jsonify({"message": "Usuario actualizado exitosamente", "new_token": new_token}), 200   
    

@login_bp.route("/usuarios/<int:id>", methods=["GET"])
@token_required
def get_user_data_by_id(id):
    """
    Obtener un usuario por su ID (requiere token de autenticación).
    Este endpoint devuelve los detalles de un usuario específico utilizando su ID.
    ---
    tags:
      - Usuarios
    security:
      - JWT: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID único del usuario a obtener.
    responses:
      200:
        description: Detalles del usuario.
        schema:
          $ref: '#/definitions/Usuario'
      401:
        description: No autorizado (token faltante o inválido).
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Usuario no encontrado.
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
        
    return jsonify({
        "id": usuario.id,
        "username": usuario.username,
        "role": usuario.role
    }), 200  


@login_bp.route("/usuarios/<int:id>", methods=["DELETE"])
@token_required
def delete_user_by_id(id):
    """
    Eliminar un usuario por su ID (requiere token de autenticación).
    Este endpoint permite eliminar un usuario específico.
    ---
    tags:
      - Usuarios
    security:
      - JWT: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID del usuario a eliminar.
    responses:
      200:
        description: Usuario eliminado exitosamente.
        schema:
          $ref: '#/definitions/MessageResponse'
      401:
        description: No autorizado (token faltante o inválido).
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Usuario no encontrado.
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    usuario = Usuario.query.get(id)
    
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"message": "Usuario eliminado exitosamente"}), 200


@login_bp.route("/usuarios", methods=["GET"])
@token_required
def get_all_users():
    """
    Obtener todos los usuarios registrados (requiere token de autenticación).
    Este endpoint devuelve una lista de todos los usuarios, excluyendo sus hashes de contraseña.
    ---
    tags:
      - Usuarios
    security:
      - JWT: []
    responses:
      200:
        description: Lista de usuarios.
        schema:
          type: array
          items:
            $ref: '#/definitions/Usuario'
      401:
        description: No autorizado (token faltante o inválido).
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: No hay usuarios registrados.
        schema:
          $ref: '#/definitions/MessageResponse'
      500:
        description: Error interno del servidor.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    
    usuarios = Usuario.query.all()

    if not usuarios:
        return jsonify({"message": "No hay usuarios registrados"}), 404

    lista = [
        {
            "id": usuario.id,
            "username": usuario.username,
            "role": usuario.role
        }
        for usuario in usuarios
    ]

    json_data = json.dumps(lista, ensure_ascii=False, sort_keys=False)
    return Response(json_data, mimetype='application/json')