from . import db

class Cuadrante(db.Model):
    __tablename__ = 'Cuadrante'

    id_cuadrante = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    detalles = db.relationship('DetalleSuela', backref='cuadrante')
