from app.database import db
from datetime import datetime
from sqlalchemy import TIME

# Modelo Negocio: información general + horarios por día
# Una fila por día de la semana (7 filas totales)
class Negocio(db.Model):
    __tablename__ = 'negocio'
    
    # ID único de cada registro
    id = db.Column(db.Integer, primary_key=True)
    
    # INFORMACIÓN GENERAL (se repite en todos los registros)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(30))
    email = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    
    # CONFIGURACIÓN GENERAL (se repite en todos los registros)
    duracion_turno = db.Column(db.Integer, default=60)  # En minutos
    intervalo_turnos = db.Column(db.Integer, default=30)  # En minutos
    max_turnos = db.Column(db.Integer, default=20)
    
    # HORARIOS ESPECÍFICOS POR DÍA
    # Día de la semana (0 = lunes, 6 = domingo, NULL = no configurado)
    dia_semana = db.Column(db.Integer)
    
    # Horarios en formato TIME
    hora_apertura = db.Column(TIME)
    hora_cierre = db.Column(TIME)
    hora_descanso_inicio = db.Column(TIME)
    hora_descanso_fin = db.Column(TIME)
    
    # Si el negocio está abierto ese día
    abierto = db.Column(db.Boolean, default=True)
    
    # Timestamps
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Convertir a diccionario para JSON
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion,
            'duracion_turno': self.duracion_turno,
            'intervalo_turnos': self.intervalo_turnos,
            'max_turnos': self.max_turnos,
            'dia_semana': self.dia_semana,
            'hora_apertura': str(self.hora_apertura) if self.hora_apertura else None,
            'hora_cierre': str(self.hora_cierre) if self.hora_cierre else None,
            'hora_descanso_inicio': str(self.hora_descanso_inicio) if self.hora_descanso_inicio else None,
            'hora_descanso_fin': str(self.hora_descanso_fin) if self.hora_descanso_fin else None,
            'abierto': self.abierto,
            'creado_en': self.creado_en.isoformat() if self.creado_en else None,
            'actualizado_en': self.actualizado_en.isoformat() if self.actualizado_en else None,
        }