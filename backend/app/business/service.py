from app.business.models import Negocio
from app.database import db
from datetime import datetime, time, timedelta

# Servicio para manejar la lógica de negocio
class NegocioService:
    
    # Obtener configuración general del negocio
    @staticmethod
    def obtener_configuracion():
        # Obtenemos el primer registro (tienen todos los mismos datos generales)
        config = Negocio.query.first()
        if not config:
            return None
        
        return {
            'nombre': config.nombre,
            'telefono': config.telefono,
            'email': config.email,
            'direccion': config.direccion,
            'duracion_turno': config.duracion_turno,
            'intervalo_turnos': config.intervalo_turnos,
            'max_turnos': config.max_turnos,
        }
    
    # Obtener horario de un día específico
    @staticmethod
    def obtener_horario_por_dia(dia_semana):
        # Buscamos el registro donde dia_semana coincida
        horario = Negocio.query.filter_by(dia_semana=dia_semana).first()
        return horario
    
    # Obtener todos los horarios de la semana
    @staticmethod
    def obtener_todos_horarios():
        # SELECT * FROM negocio WHERE dia_semana IS NOT NULL ORDER BY dia_semana
        horarios = Negocio.query.filter(
            Negocio.dia_semana.isnot(None)
        ).order_by(Negocio.dia_semana).all()
        return horarios
    
    # Verificar si está abierto hoy
    @staticmethod
    def esta_abierto_hoy():
        # Obtenemos el día de hoy (0 = lunes, 6 = domingo en weekday)
        dia_hoy = datetime.now().weekday()
        
        # Buscamos el horario para hoy
        horario = NegocioService.obtener_horario_por_dia(dia_hoy)
        
        # Si no existe o no está abierto, retornamos False
        if not horario or not horario.abierto:
            return False
        
        return True
    
    # Obtener horarios disponibles para un día
    @staticmethod
    def obtener_horarios_disponibles(dia_semana, duracion_turno=None):
        # Obtenemos el horario del día
        horario = NegocioService.obtener_horario_por_dia(dia_semana)
        
        # Si está cerrado o no tiene datos, retornamos lista vacía
        if not horario or not horario.abierto or not horario.hora_apertura or not horario.hora_cierre:
            return []
        
        # Si no especifican duración, usamos la del negocio
        if duracion_turno is None:
            duracion_turno = horario.duracion_turno
        
        # Generamos slots basado en intervalo_turnos (generalmente 30 min)
        slots = []
        
        # Convertimos TIME a datetime para manipular
        apertura = datetime.combine(datetime.today(), horario.hora_apertura)
        cierre = datetime.combine(datetime.today(), horario.hora_cierre)
        intervalo = horario.intervalo_turnos
        
        current = apertura
        
        # Iteramos cada X minutos (intervalo_turnos)
        while current < cierre:
            # Verificamos si está dentro del horario de descanso
            if horario.hora_descanso_inicio and horario.hora_descanso_fin:
                current_time = current.time()
                # Si está en descanso, saltamos
                if horario.hora_descanso_inicio <= current_time < horario.hora_descanso_fin:
                    current += timedelta(minutes=intervalo)
                    continue
            
            # Agregamos el slot
            slots.append(current.time().strftime('%H:%M'))
            
            # Avanzamos según el intervalo
            current += timedelta(minutes=intervalo)
        
        return slots
    
    # Guardar/actualizar horarios y configuración
    @staticmethod
    def guardar_configuracion_completa(datos):
        # datos debe contener:
        # {
        #   'nombre': ...,
        #   'telefono': ...,
        #   'email': ...,
        #   'direccion': ...,
        #   'duracion_turno': ...,
        #   'intervalo_turnos': ...,
        #   'max_turnos': ...,
        #   'horarios': [
        #     {
        #       'dia_semana': 0,
        #       'hora_apertura': '09:00',
        #       'hora_cierre': '18:00',
        #       'hora_descanso_inicio': '12:00',
        #       'hora_descanso_fin': '13:00',
        #       'abierto': true
        #     },
        #     ...
        #   ]
        # }
        
        try:
            # Obtener información general
            nombre = datos.get('nombre')
            telefono = datos.get('telefono')
            email = datos.get('email')
            direccion = datos.get('direccion')
            duracion_turno = datos.get('duracion_turno', 60)
            intervalo_turnos = datos.get('intervalo_turnos', 30)
            max_turnos = datos.get('max_turnos', 20)
            
            # Actualizar cada día
            for horario_data in datos.get('horarios', []):
                # Buscamos si existe el registro para ese día
                negocio = Negocio.query.filter_by(
                    dia_semana=horario_data['dia_semana']
                ).first()
                
                # Si no existe, creamos uno nuevo
                if not negocio:
                    negocio = Negocio()
                
                # Actualizamos los datos generales (se repiten en todos los registros)
                negocio.nombre = nombre
                negocio.telefono = telefono
                negocio.email = email
                negocio.direccion = direccion
                negocio.duracion_turno = duracion_turno
                negocio.intervalo_turnos = intervalo_turnos
                negocio.max_turnos = max_turnos
                
                # Actualizamos datos específicos del día
                negocio.dia_semana = horario_data['dia_semana']
                negocio.abierto = horario_data.get('abierto', True)
                negocio.hora_apertura = horario_data.get('hora_apertura')
                negocio.hora_cierre = horario_data.get('hora_cierre')
                negocio.hora_descanso_inicio = horario_data.get('hora_descanso_inicio')
                negocio.hora_descanso_fin = horario_data.get('hora_descanso_fin')
                
                # Agregamos a la sesión
                db.session.add(negocio)
            
            # Guardamos todos los cambios
            db.session.commit()
            
            return {
                'success': True,
                'mensaje': 'Configuración guardada correctamente'
            }
        
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'mensaje': f'Error al guardar configuración: {str(e)}'
            }
    
    # Obtener horarios en formato dict (para devolver al frontend)
    @staticmethod
    def obtener_horarios_dict():
        horarios = NegocioService.obtener_todos_horarios()
        return [h.to_dict() for h in horarios]