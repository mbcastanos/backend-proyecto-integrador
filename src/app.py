from flask import Flask
from flask_cors import CORS
from controllers.tarea_controller import tarea_bp

app = Flask(__name__)
CORS(app)  # Permite que React u otros frontends puedan conectarse

# Registro de las rutas del controlador
app.register_blueprint(tarea_bp)

if __name__ == "__main__":
    app.run(debug=True)
