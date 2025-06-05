import datetime
import bcrypt
from flask import Blueprint, jsonify, request
from models import db, Usuario

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
    
    return jsonify({"message" : "inicio valido"}), 200
    

@login_bp.route("/usuarios", methods = ["POST"])
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




