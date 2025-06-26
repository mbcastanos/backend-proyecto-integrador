from . import db

class Modelo(db.Model):
    __tablename__ = 'Modelo'

    id_modelo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    def to_dict(self):
        return {
            'id_modelo': self.id_modelo,
            'nombre': self.nombre
        } 