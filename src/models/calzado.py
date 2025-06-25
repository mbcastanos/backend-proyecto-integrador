from . import db

class Calzado(db.Model):
    __tablename__ = 'Calzado'

    id_calzado = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    talle = db.Column(db.String(10), nullable=False)
    ancho = db.Column(db.Numeric(5, 2), nullable=False)
    alto = db.Column(db.Numeric(5, 2), nullable=False)
    colores = db.Column(db.String(100), nullable=False)
    tipo_registro = db.Column(
        db.Enum('indubitada_proveedor', 'indubitada_comisaria', 'dubitada'),
        nullable=False
    )

    suelas = db.relationship('Suela', backref='calzado', cascade="all, delete-orphan")
    categorias = db.relationship('Categoria', backref='calzado', cascade="all, delete-orphan")
