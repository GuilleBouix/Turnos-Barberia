from app.database import db
from datetime import datetime
from sqlalchemy import TIME, String, Text

class Negocio(db.Model):
    __tablename__ = 'negocio'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Información general
    nombre = db.Column(String(255), nullable=False, default='Barbería')
    telefono = db.Column(String(50))
    email = db.Column(String(255))
    direccion = db.Column(Text)
    
    # Configuración de turnos
    duracion_turno = db.Column(db.Integer, default=60)  # minutos
    intervalo_turnos = db.Column(db.Integer, default=30)  # minutos
    max_turnos = db.Column(db.Integer, default=20)
    
    # Horarios por día (campos existentes)
    dia_semana = db.Column(db.Integer, nullable=False)
    hora_apertura = db.Column(TIME, nullable=False)
    hora_cierre = db.Column(TIME, nullable=False)
    hora_descanso_inicio = db.Column(TIME)
    hora_descanso_fin = db.Column(TIME)
    abierto = db.Column(db.Boolean, default=True)
    
    # Timestamps
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            # Información general
            'nombre': self.nombre,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion,
            
            # Configuración de turnos
            'duracion_turno': self.duracion_turno,
            'intervalo_turnos': self.intervalo_turnos,
            'max_turnos': self.max_turnos,
            
            # Horarios
            'dia_semana': self.dia_semana,
            'hora_apertura': str(self.hora_apertura) if self.hora_apertura else None,
            'hora_cierre': str(self.hora_cierre) if self.hora_cierre else None,
            'hora_descanso_inicio': str(self.hora_descanso_inicio) if self.hora_descanso_inicio else None,
            'hora_descanso_fin': str(self.hora_descanso_fin) if self.hora_descanso_fin else None,
            'abierto': self.abierto,
            
            # Timestamps
            'creado_en': self.creado_en.isoformat() if self.creado_en else None,
            'actualizado_en': self.actualizado_en.isoformat() if self.actualizado_en else None,
        }