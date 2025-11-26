from app.database import db
from datetime import datetime
from sqlalchemy import Date, Time, String, ForeignKey
from sqlalchemy.orm import relationship

class GestionTurnos(db.Model):
    __tablename__ = 'turnos'
    __table_args__ = {'extend_existing': True}  # ← ESTA LÍNEA SOLUCIONA EL PROBLEMA
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(Date, nullable=False)
    hora = db.Column(Time, nullable=False)
    servicio_id = db.Column(db.Integer, ForeignKey('servicios.id'), nullable=False)
    nombre_cliente = db.Column(db.String(100), nullable=False)
    telefono_cliente = db.Column(db.String(20), nullable=False)
    client_id = db.Column(db.String(50))
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, confirmado, completado, cancelado
    token_cancelacion = db.Column(db.String(100))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con servicios
    servicio = relationship('Servicio', backref='turnos')
    
    def to_dict(self):
        return {
            'id': self.id,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'hora': str(self.hora) if self.hora else None,
            'servicio_id': self.servicio_id,
            'nombre_servicio': self.servicio.nombre_servicio if self.servicio else '',
            'categoria_servicio': self.servicio.categoria if self.servicio else '',
            'precio_servicio': float(self.servicio.precio) if self.servicio and self.servicio.precio else 0.0,
            'nombre_cliente': self.nombre_cliente,
            'telefono_cliente': self.telefono_cliente,
            'client_id': self.client_id,
            'estado': self.estado,
            'token_cancelacion': self.token_cancelacion,
            'creado_en': self.creado_en.isoformat() if self.creado_en else None,
            'actualizado_en': self.actualizado_en.isoformat() if self.actualizado_en else None,
        }