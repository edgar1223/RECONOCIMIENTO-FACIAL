from flask import Flask
from config import Config
from extensions import db, ma
from routes.facial import facial_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar extensiones
    db.init_app(app)
    ma.init_app(app)
    
    # Registrar blueprints
    
    
    app.register_blueprint(facial_bp)
    
    return app