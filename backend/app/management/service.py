from app.management.models import GestionTurnos
from app.database import db
from datetime import datetime, date

class GestionTurnosService:
    
    @staticmethod
    def obtener_todos_turnos(fecha_filtro=None):
        """Obtener todos los turnos con JOIN a servicios"""
        try:
            query = GestionTurnos.query.join(GestionTurnos.servicio)
            
            # Filtrar por fecha si se especifica
            if fecha_filtro:
                fecha = datetime.strptime(fecha_filtro, '%Y-%m-%d').date()
                query = query.filter(GestionTurnos.fecha == fecha)
            
            # Ordenar por fecha (más reciente primero) y hora
            turnos = query.order_by(GestionTurnos.fecha.desc(), GestionTurnos.hora.asc()).all()
            return turnos
        except Exception as e:
            print(f"Error al obtener turnos: {str(e)}")
            return []
    
    @staticmethod
    def obtener_turno_por_id(turno_id):
        """Obtener un turno por su ID"""
        try:
            turno = GestionTurnos.query.get(turno_id)
            return turno
        except Exception as e:
            print(f"Error al obtener turno: {str(e)}")
            return None
    
    @staticmethod
    def marcar_como_completado(turno_id):
        """Marcar un turno como completado"""
        try:
            turno = GestionTurnos.query.get(turno_id)
            if not turno:
                return {'success': False, 'mensaje': 'Turno no encontrado'}
            
            turno.estado = 'completado'
            db.session.commit()
            
            return {'success': True, 'mensaje': 'Turno marcado como completado'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'mensaje': f'Error al completar turno: {str(e)}'}
    
    @staticmethod
    def eliminar_turno(turno_id):
        """Eliminar un turno"""
        try:
            turno = GestionTurnos.query.get(turno_id)
            if not turno:
                return {'success': False, 'mensaje': 'Turno no encontrado'}
            
            db.session.delete(turno)
            db.session.commit()
            
            return {'success': True, 'mensaje': 'Turno eliminado correctamente'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'mensaje': f'Error al eliminar turno: {str(e)}'}
    
    @staticmethod
    def obtener_turnos_hoy():
        """Obtener turnos para hoy"""
        try:
            hoy = date.today()
            turnos = GestionTurnos.query.filter(GestionTurnos.fecha == hoy)\
                .join(GestionTurnos.servicio)\
                .order_by(GestionTurnos.hora.asc()).all()
            return turnos
        except Exception as e:
            print(f"Error al obtener turnos de hoy: {str(e)}")
            return []