from functools import wraps
from flask import g, request, jsonify
import jwt
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv("SECRET_KEY")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
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
