from . import db

class FormaGeometrica(db.Model):
    __tablename__ = 'FormaGeometrica'

    id_forma = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    detalles = db.relationship('DetalleSuela', backref='forma')

    def to_dict(self): #Metodo para el endpoint update_forma
        return {
            'id_forma': self.id_forma,
            'nombre': self.nombre
        }