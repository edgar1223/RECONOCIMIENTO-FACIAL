from extensions import db

class Usuario(db.Model):
    __tablename__ = 'api_usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo_electronico = db.Column(db.String(100), nullable=False, unique=True)
    firma = db.Column(db.String(600))
    rubrica = db.Column(db.String(600))
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    ruta = db.Column(db.String(255), nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    departamento_id = db.Column(db.Integer, db.ForeignKey('api_departamento.idDep'))
    fcm_token = db.Column(db.Text)
    
    departamento = db.relationship('Departamento', backref=db.backref('usuarios', lazy=True))
    facial_features = db.relationship('FacialFeatures', backref='usuario', lazy=True)