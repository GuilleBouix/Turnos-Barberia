from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.database import db
from app.extensions import jwt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    
    # Configurar CORS para permitir el frontend en puerto diferente
    CORS(app, 
         origins=["http://localhost:4321", "http://127.0.0.1:4321"],
         allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         expose_headers=["Content-Type", "Authorization"],
         supports_credentials=True)
    
    # Registrar blueprints
    from app.auth.routes import auth_bp
    from app.business.routes import business_bp
    from app.services.routes import servicios_bp
    from app.appointments.routes import appointments_bp
    from app.management.routes import management_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(business_bp)
    app.register_blueprint(servicios_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(management_bp)
    
    # Crear tablas
    with app.app_context():
        db.create_all()
    
    return app