from . import db

class Categoria(db.Model):
    __tablename__ = 'Categoria'
    
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    id_calzado= db.Column(db.Integer, db.ForeignKey("Calzado.id_calzado"), nullable=False)