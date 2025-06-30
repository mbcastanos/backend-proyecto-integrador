from . import db

class Imputado(db.Model):
    __tablename__ = 'Imputado'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    nombre = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), nullable=False, unique=True)
    direccion = db.Column(db.String(200), nullable=True)
    comisaria = db.Column(db.String(100), nullable=True)
    jurisdiccion = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'dni': self.dni,
            'direccion': self.direccion,
            'comisaria': self.comisaria,
            'jurisdiccion': self.jurisdiccion

        } 

