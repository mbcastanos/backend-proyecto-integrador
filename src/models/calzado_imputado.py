from . import db 

class CalzadoImputado(db.Model):
    __tablename__ = 'calzado_has_imputado'
    calzado_id_calzado = db.Column(db.Integer, db.ForeignKey('Calzado.id_calzado'), primary_key=True)
    imputado_id = db.Column(db.Integer, db.ForeignKey('Imputado.id'), primary_key=True)