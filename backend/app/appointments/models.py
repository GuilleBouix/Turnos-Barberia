from app.database import db
from datetime import datetime
import secrets

# Modelo Turno: representa una reserva de turno en la barbería
class Turno(db.Model):
    __tablename__ = 'turnos'
    
    # ID único del turno
    id = db.Column(db.Integer, primary_key=True)
    
    # Fecha del turno (YYYY-MM-DD)
    fecha = db.Column(db.Date, nullable=False)
    
    # Hora del turno (HH:MM:SS)
    hora = db.Column(db.Time, nullable=False)
    
    # ID del servicio que va a usar (relación a tabla servicios)
    servicio_id = db.Column(db.Integer, nullable=False)
    
    # Datos del cliente que reserva
    nombre_cliente = db.Column(db.String(120), nullable=False)
    telefono_cliente = db.Column(db.String(30), nullable=False)
    
    # ID del cliente (generado como cookie en el frontend)
    # Esto permite que un user solo tenga 1 turno activo sin necesidad de login
    client_id = db.Column(db.String(100), nullable=False)
    
    # Estado del turno: 'reservado', 'completado', 'cancelado', 'no-show'
    estado = db.Column(db.String(20), nullable=False, default='reservado')
    
    # Token único para cancelar el turno (sin necesidad de estar logueado)
    # Se genera aleatoriamente y se pasa por URL
    token_cancelacion = db.Column(db.String(200), unique=True, nullable=False)
    
    # Timestamps
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        # Generamos automáticamente el token de cancelación
        super().__init__(**kwargs)
        self.token_cancelacion = self._generar_token()
    
    # Generar token seguro de 200 caracteres
    @staticmethod
    def _generar_token():
        return secrets.token_urlsafe(150)
    
    # Convertir objeto a diccionario para JSON
    def to_dict(self):
        return {
            'id': self.id,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'hora': self.hora.isoformat() if self.hora else None,
            'servicio_id': self.servicio_id,
            'nombre_cliente': self.nombre_cliente,
            'telefono_cliente': self.telefono_cliente,
            'client_id': self.client_id,
            'estado': self.estado,
            'token_cancelacion': self.token_cancelacion,
            'creado_en': self.creado_en.isoformat() if self.creado_en else None,
            'actualizado_en': self.actualizado_en.isoformat() if self.actualizado_en else None,
        }
    
    # Método para verificar si el turno está activo
    def esta_activo(self):
        return self.estado == 'reservado'
    
    # Método para cancelar el turno
    def cancelar(self):
        self.estado = 'cancelado'
        self.actualizado_en = datetime.utcnow()