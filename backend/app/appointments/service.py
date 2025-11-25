from app.appointments.models import Turno
from app.database import db
from datetime import datetime, timedelta, time
from sqlalchemy import and_, or_

# Servicio para manejar la lógica de turnos
class TurnoService:
    
    # Obtener turno activo de un cliente
    @staticmethod
    def obtener_turno_activo(client_id):
        # Buscamos un turno reservado para este cliente
        turno = Turno.query.filter_by(
            client_id=client_id,
            estado='reservado'
        ).first()
        
        return turno
    
    # Verificar si un cliente ya tiene turno activo
    @staticmethod
    def cliente_tiene_turno_activo(client_id):
        turno = TurnoService.obtener_turno_activo(client_id)
        return turno is not None
    
    # Obtener todos los horarios disponibles para una fecha
    @staticmethod
    def obtener_horarios_disponibles(fecha, duracion_turno=60):
        # Convertimos fecha string a objeto Date
        if isinstance(fecha, str):
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        else:
            fecha_obj = fecha
        
        # Obtenemos el día de la semana (0 = lunes, 6 = domingo)
        dia_semana = fecha_obj.weekday()
        
        # Importamos el servicio de negocio para obtener horarios
        from app.business.service import NegocioService
        
        # Obtenemos los slots disponibles del negocio
        slots = NegocioService.obtener_horarios_disponibles(dia_semana)
        
        if not slots:
            return []
        
        # Ahora filtramos cuáles de esos slots ya están reservados
        horarios_disponibles = []
        
        for slot in slots:
            # Convertimos el slot a objeto time
            slot_time = datetime.strptime(slot, '%H:%M').time()
            
            # Buscamos si ya hay un turno reservado en ese horario
            turno_existe = Turno.query.filter_by(
                fecha=fecha_obj,
                hora=slot_time,
                estado='reservado'
            ).first()
            
            # Si no existe turno en ese horario, está disponible
            if not turno_existe:
                horarios_disponibles.append({
                    'hora': slot,
                    'disponible': True,
                    'estado': 'disponible'
                })
            else:
                horarios_disponibles.append({
                    'hora': slot,
                    'disponible': False,
                    'estado': 'reservado'
                })
        
        return horarios_disponibles
    
    # Crear un nuevo turno
    @staticmethod
    def crear_turno(fecha, hora, servicio_id, nombre_cliente, telefono_cliente, client_id):
        # Validación 1: ¿El cliente ya tiene turno activo?
        if TurnoService.cliente_tiene_turno_activo(client_id):
            return {
                'success': False,
                'mensaje': 'Ya tenés un turno activo. Cancelalo para hacer otro.'
            }
        
        # Convertimos fecha y hora a objetos si son strings
        if isinstance(fecha, str):
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        else:
            fecha_obj = fecha
        
        if isinstance(hora, str):
            hora_obj = datetime.strptime(hora, '%H:%M').time()
        else:
            hora_obj = hora
        
        # Validación 2: ¿Ese horario ya está reservado?
        turno_existe = Turno.query.filter_by(
            fecha=fecha_obj,
            hora=hora_obj,
            servicio_id=servicio_id,
            estado='reservado'
        ).first()
        
        if turno_existe:
            return {
                'success': False,
                'mensaje': 'Ese horario ya está reservado. Elegí otro.'
            }
        
        # Validación 3: ¿La fecha no es en el pasado?
        if fecha_obj < datetime.now().date():
            return {
                'success': False,
                'mensaje': 'No podés reservar en fechas pasadas.'
            }
        
        try:
            # Crear el turno
            turno = Turno(
                fecha=fecha_obj,
                hora=hora_obj,
                servicio_id=servicio_id,
                nombre_cliente=nombre_cliente,
                telefono_cliente=telefono_cliente,
                client_id=client_id,
                estado='reservado'
            )
            
            # Guardar en la BD
            db.session.add(turno)
            db.session.commit()
            
            return {
                'success': True,
                'mensaje': 'Turno reservado exitosamente',
                'turno': turno.to_dict()
            }
        
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'mensaje': f'Error al crear turno: {str(e)}'
            }
    
    # Cancelar turno por token
    @staticmethod
    def cancelar_turno_por_token(token_cancelacion):
        # Buscamos el turno por el token
        turno = Turno.query.filter_by(
            token_cancelacion=token_cancelacion,
            estado='reservado'
        ).first()
        
        if not turno:
            return {
                'success': False,
                'mensaje': 'Token inválido o turno ya cancelado'
            }
        
        try:
            # Cancelamos el turno
            turno.cancelar()
            db.session.commit()
            
            return {
                'success': True,
                'mensaje': 'Turno cancelado exitosamente'
            }
        
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'mensaje': f'Error al cancelar: {str(e)}'
            }
    
    # Obtener turnos de un rango de fechas (para admin)
    @staticmethod
    def obtener_turnos_rango(fecha_inicio, fecha_fin, estado='reservado'):
        # Query para obtener turnos en ese rango
        turnos = Turno.query.filter(
            Turno.fecha >= fecha_inicio,
            Turno.fecha <= fecha_fin,
            Turno.estado == estado
        ).order_by(Turno.fecha, Turno.hora).all()
        
        return turnos
    
    # Obtener próximo turno disponible
    @staticmethod
    def obtener_proximo_turno_disponible(dias_adelante=7):
        # Buscamos el próximo día con turnos disponibles
        from app.business.service import NegocioService
        
        hoy = datetime.now().date()
        
        for i in range(dias_adelante):
            fecha_check = hoy + timedelta(days=i)
            horarios = TurnoService.obtener_horarios_disponibles(fecha_check)
            
            # Si hay horarios disponibles, retornamos esa fecha
            if any(h['disponible'] for h in horarios):
                return {
                    'fecha': fecha_check.isoformat(),
                    'horarios': horarios
                }
        
        return None