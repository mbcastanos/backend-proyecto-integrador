from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .calzado import Calzado
from .suela import Suela
from .cuadrante import Cuadrante
from .forma_geometrica import FormaGeometrica
from .detalle_suela import DetalleSuela

