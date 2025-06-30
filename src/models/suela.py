from . import db

# suela.py
from . import db

class Suela(db.Model):
    __tablename__ = 'Suela'

    id_suela = db.Column(db.Integer, primary_key=True)
    id_calzado = db.Column(db.Integer, db.ForeignKey('Calzado.id_calzado'), nullable=False)
    descripcion_general = db.Column(db.Text, nullable=True)

    detalles = db.relationship('DetalleSuela', backref='suela', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id_suela': self.id_suela,
            'id_calzado': self.id_calzado,
            'descripcion_general': self.descripcion_general,
            'detalles': [detalle.to_dict() for detalle in self.detalles]
        }
