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
    usuario = Usuario.query.get(id)
    
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"message": "Usuario eliminado exitosamente"}), 200


@login_bp.route("/usuarios", methods=["GET"])
@token_required
def get_all_users():
    
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