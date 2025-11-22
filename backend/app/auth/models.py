from app.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Definimos la clase Usuario que hereda de db.Model
# Esto le dice a SQLAlchemy que esta clase representa una tabla en la BD
class Usuario(db.Model):
    # Le decimos explícitamente a SQLAlchemy el nombre de la tabla
    __tablename__ = 'usuarios'

    # Columna id: llave primaria, autoincremental
    id = db.Column(db.Integer, primary_key=True)
    
    # Columna nombre_usuario: string único (no puede haber dos con el mismo nombre)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    
    # Columna contrasena: string para guardar el hash (nunca guardamos la contrasena en texto plano)
    contrasena = db.Column(db.String(255), nullable=False)
    
    # Columna creado_en: timestamp automático cuando se crea el usuario
    creado_en = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Columna actualizado_en: timestamp que se actualiza cada vez que modificamos el usuario
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Método para hashear la contrasena antes de guardarla
    # Usamos generate_password_hash de werkzeug, que es súper seguro
    def establecer_contrasena(self, contrasena):
        self.contrasena = generate_password_hash(contrasena)

    # Método para verificar que la contrasena ingresada coincide con el hash guardado
    # Retorna True si es correcta, False si no
    def verificar_contrasena(self, contrasena):
        return check_password_hash(self.contrasena, contrasena)

    # Método auxiliar para devolver los datos del usuario como diccionario
    # Útil para retornar info en JSON
    def to_dict(self):
        return {
            'id': self.id,
            'nombre_usuario': self.nombre_usuario,
            'creado_en': self.creado_en.isoformat(),
            'actualizado_en': self.actualizado_en.isoformat()
        }