from . import db

class Color(db.Model):
    __tablename__ = 'Colores'

    id_color = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    def to_dict(self):
        return {
            'id_color': self.id_color,
            'nombre': self.nombre
        }
