from . import db

class DetalleSuela(db.Model):
    __tablename__ = 'DetalleSuela'

    id_detalle = db.Column(db.Integer, primary_key=True)
    id_suela = db.Column(db.Integer, db.ForeignKey('Suela.id_suela'), nullable=False)
    id_cuadrante = db.Column(db.Integer, db.ForeignKey('Cuadrante.id_cuadrante'), nullable=False)
    id_forma = db.Column(db.Integer, db.ForeignKey('FormaGeometrica.id_forma'), nullable=False)
    detalle_adicional = db.Column(db.Text, nullable=True)
