from . import db


# Tabla intermedia para la relación muchos a muchos entre Calzado y Color
calzado_color = db.Table('calzado_color',
    db.Column('id_calzado', db.Integer, db.ForeignKey('Calzado.id_calzado'), primary_key=True),
    db.Column('id_color', db.Integer, db.ForeignKey('Colores.id_color'), primary_key=True)
)

class Calzado(db.Model):
    __tablename__ = 'Calzado'

    id_calzado = db.Column(db.Integer, primary_key=True)
    talle = db.Column(db.String(10), nullable=True)
    ancho = db.Column(db.Numeric(5, 2), nullable=True)
    alto = db.Column(db.Numeric(5, 2), nullable=True)
    tipo_registro = db.Column(
        db.Enum('indubitada_proveedor', 'indubitada_comisaria', 'dubitada'),
        nullable=True
    )
    id_marca = db.Column(db.Integer, db.ForeignKey('Marca.id_marca'), nullable=True)
    id_modelo = db.Column(db.Integer, db.ForeignKey('Modelo.id_modelo'), nullable=True)
    id_categoria = db.Column(db.Integer, db.ForeignKey('Categoria.id_categoria'), nullable=True)

    suelas = db.relationship('Suela', backref='calzado', cascade="all, delete-orphan")
    marca = db.relationship('Marca', backref='calzados')
    modelo = db.relationship('Modelo', backref='calzados')
    categoria = db.relationship('Categoria', backref='calzados')
    colores = db.relationship('Color', secondary=calzado_color, backref='calzados')

    def to_dict(self):
        return {
            'id_calzado': self.id_calzado,
            'talle': self.talle,
            'ancho': float(self.ancho) if self.ancho else None,
            'alto': float(self.alto) if self.alto else None,
            'tipo_registro': self.tipo_registro,
            'id_marca': self.id_marca,
            'marca': self.marca.nombre if self.marca else None,
            'id_modelo': self.id_modelo,
            'modelo': self.modelo.nombre if self.modelo else None,
            'id_categoria': self.id_categoria,
            'categoria': self.categoria.nombre if self.categoria else None,
            'colores': [color.nombre for color in self.colores] if self.colores else []
        }
