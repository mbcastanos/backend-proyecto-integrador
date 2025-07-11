from . import db 

class CalzadoImputado(db.Model):
    __tablename__ = 'calzado_has_imputado'
    calzado_id_calzado = db.Column(db.Integer, db.ForeignKey('calzado.id_calzado', ondelete='CASCADE'), primary_key=True)
    imputado_id = db.Column(db.Integer, db.ForeignKey('imputado.id', ondelete='CASCADE'), primary_key=True)