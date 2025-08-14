from ..extensions import db

class FacialFeatures(db.Model):
    __tablename__ = 'facial_features'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('api_usuario.id'), nullable=False)
    facial_vector = db.Column(db.ARRAY(db.Float), nullable=False)
    fecha_registro = db.Column(db.DateTime, server_default=db.func.now())
    metadata = db.Column(db.JSON)  # Para información adicional