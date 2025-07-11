from functools import wraps
from flask import g, request, jsonify
import jwt
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv("SECRET_KEY")

# Asegurarse de que secret_key no sea None en produccion
if not secret_key:
    print("ADVERTENCIA: SECRET_KEY no está configurada. Los tokens JWT no funcionarán correctamente.")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        # LOGICA CRITICA: PERMITIR SOLICITUDES OPTIONS SIN VALIDACION DE TOKEN ---
        # Los navegadores envian una solicitud OPTIONS (preflight) antes de la solicitud real
        # para verificar los permisos de CORS. Esta solicitud no incluye el token de autenticacion.
        # Si se intenta validar el token en una solicitud OPTIONS, devuelve un 401,
        # lo que hara que el navegador bloquee la solicitud real por CORS.
        if request.method == 'OPTIONS':
            return f(*args, **kwargs) # Permite que la solicitud OPTIONS pase sin token
        
        token = None

        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Token es requerido"}), 401

        try:
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            g.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        return f(*args, **kwargs)

    return decorated
