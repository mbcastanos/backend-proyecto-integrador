from . import db

class Categoria(db.Model):
    __tablename__ = 'Categoria'
    
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    def to_dict(self):
        return {
            'id_categoria': self.id_categoria,
            'nombre': self.nombre
        }