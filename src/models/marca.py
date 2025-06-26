from . import db

class Marca(db.Model):
    __tablename__ = 'Marca'

    id_marca = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    def to_dict(self):
        return {
            'id_marca': self.id_marca,
            'nombre': self.nombre
        }
