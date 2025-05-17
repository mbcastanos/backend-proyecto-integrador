from flask import Flask, jsonify
from models import db, Calzado

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/bd_calzado'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/calzados', methods=['GET'])
def get_calzados():
    calzados = Calzado.query.all()
    resultado = []
    for c in calzados:
        resultado.append({
            'id_calzado': c.id_calzado,
            'categoria': c.categoria,
            'marca': c.marca,
            'modelo': c.modelo,
            'talle': c.talle,
            'ancho': float(c.ancho),
            'alto': float(c.alto),
            'colores': c.colores,
            'tipo_registro': c.tipo_registro
        })
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
