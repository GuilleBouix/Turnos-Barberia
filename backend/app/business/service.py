from app.business.models import Negocio
from app.database import db
from datetime import datetime, time, timedelta

class NegocioService:
    
    @staticmethod
    def obtener_horario_por_dia(dia_semana):
        return Negocio.query.filter_by(dia_semana=dia_semana).first()
    
    @staticmethod
    def obtener_todos_horarios():
        return Negocio.query.order_by(Negocio.dia_semana).all()
    
    @staticmethod
    def obtener_configuracion_general():
        """Obtiene la configuración general (usamos el primer registro como base)"""
        # Podemos usar cualquier registro, pero normalmente usamos el primero
        config = Negocio.query.first()
        if not config:
            # Si no hay registros, crear uno por defecto
            config = Negocio(
                nombre='Barbería',
                duracion_turno=60,
                intervalo_turnos=30,
                max_turnos=20,
            )
            db.session.add(config)
            db.session.commit()
        return config
    
    @staticmethod
    def esta_abierto_hoy():
        dia_hoy = datetime.now().weekday()
        horario = NegocioService.obtener_horario_por_dia(dia_hoy)
        return bool(horario and horario.abierto)
    
    @staticmethod
    def obtener_horarios_disponibles(dia_semana, duracion_turno=60):
        horario = NegocioService.obtener_horario_por_dia(dia_semana)
        
        if not horario or not horario.abierto:
            return []
        
        slots = []
        apertura = datetime.combine(datetime.today(), horario.hora_apertura)
        cierre = datetime.combine(datetime.today(), horario.hora_cierre)
        
        current = apertura
        
        while current < cierre:
            if horario.hora_descanso_inicio and horario.hora_descanso_fin:
                current_time = current.time()
                if horario.hora_descanso_inicio <= current_time < horario.hora_descanso_fin:
                    current += timedelta(minutes=30)
                    continue
            
            slots.append(current.time().strftime('%H:%M'))
            current += timedelta(minutes=30)
        
        return slots
    
    @staticmethod
    def guardar_configuracion_completa(datos):
        try:
            print("💾 Iniciando guardado de configuración completa...")
            
            # 1. Primero actualizar la configuración general
            config_general = Negocio.query.filter(Negocio.dia_semana.is_(None)).first()
            
            if not config_general:
                print("🆕 Creando nueva configuración general...")
                config_general = Negocio()
            
            # Actualizar campos de configuración general
            if 'nombre' in datos:
                config_general.nombre = datos['nombre']
            if 'telefono' in datos:
                config_general.telefono = datos['telefono']
            if 'email' in datos:
                config_general.email = datos['email']
            if 'direccion' in datos:
                config_general.direccion = datos['direccion']
            if 'duracion_turno' in datos:
                config_general.duracion_turno = datos['duracion_turno']
            if 'intervalo_turnos' in datos:
                config_general.intervalo_turnos = datos['intervalo_turnos']
            if 'max_turnos' in datos:
                config_general.max_turnos = datos['max_turnos']
            
            db.session.add(config_general)
            print("✅ Configuración general actualizada")
            
            # 2. Actualizar horarios
            if 'horarios' in datos:
                print(f"📅 Procesando {len(datos['horarios'])} horarios...")
                
                for horario_data in datos['horarios']:
                    dia_semana = horario_data['dia_semana']
                    print(f"  📝 Procesando día {dia_semana}...")
                    
                    # Buscar horario existente para este día
                    horario = Negocio.query.filter_by(dia_semana=dia_semana).first()
                    
                    if not horario:
                        print(f"  🆕 Creando nuevo horario para día {dia_semana}")
                        horario = Negocio(dia_semana=dia_semana)
                    
                    # Actualizar campos del horario
                    horario.abierto = horario_data.get('abierto', True)
                    horario.hora_apertura = horario_data['hora_apertura']
                    horario.hora_cierre = horario_data['hora_cierre']
                    
                    # Manejar campos nulos para descanso
                    hora_descanso_inicio = horario_data.get('hora_descanso_inicio')
                    hora_descanso_fin = horario_data.get('hora_descanso_fin')
                    
                    horario.hora_descanso_inicio = hora_descanso_inicio if hora_descanso_inicio else None
                    horario.hora_descanso_fin = hora_descanso_fin if hora_descanso_fin else None
                    
                    print(f"  ✅ Día {dia_semana} - Abierto: {horario.abierto}, Apertura: {horario.hora_apertura}, Cierre: {horario.hora_cierre}, Descanso: {horario.hora_descanso_inicio} - {horario.hora_descanso_fin}")
                    
                    db.session.add(horario)
            
            # 3. Guardar todos los cambios
            db.session.commit()
            print("💾 Todos los cambios guardados en la BD")
            
            return {
                'success': True,
                'mensaje': 'Configuración guardada correctamente'
            }
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al guardar configuración: {str(e)}")
            return {
                'success': False,
                'mensaje': f'Error al guardar configuración: {str(e)}'
            }
    
    @staticmethod
    def obtener_configuracion_completa():
        """Obtiene toda la configuración: general + horarios"""
        try:
            print("🔍 Buscando configuración completa...")
            
            # Obtener configuración general (registro con dia_semana = NULL)
            config_general = Negocio.query.filter(Negocio.dia_semana.is_(None)).first()
            
            # Si no existe, crear una por defecto
            if not config_general:
                print("🆕 Creando configuración general por defecto...")
                config_general = Negocio(
                    nombre='Mi Barbería',
                    duracion_turno=60,
                    intervalo_turnos=30,
                    max_turnos=20
                )
                db.session.add(config_general)
                db.session.commit()
            
            # Obtener todos los horarios (asegurarnos de que hay 7, uno por día)
            horarios = Negocio.query.filter(Negocio.dia_semana.isnot(None)).order_by(Negocio.dia_semana).all()
            
            # Si faltan horarios, crearlos
            if len(horarios) < 7:
                print(f"🆕 Creando horarios faltantes. Actuales: {len(horarios)}")
                dias_existentes = [h.dia_semana for h in horarios]
                
                for dia in range(7):  # 0-6
                    if dia not in dias_existentes:
                        print(f"  ➕ Creando horario para día {dia}")
                        horario_default = Negocio(
                            dia_semana=dia,
                            hora_apertura='09:00:00',
                            hora_cierre='18:00:00',
                            hora_descanso_inicio='13:00:00',
                            hora_descanso_fin='14:00:00',
                            abierto=True
                        )
                        db.session.add(horario_default)
                        horarios.append(horario_default)
                
                if len(horarios) < 7:
                    db.session.commit()
                    # Recargar horarios después del commit
                    horarios = Negocio.query.filter(Negocio.dia_semana.isnot(None)).order_by(Negocio.dia_semana).all()
            
            print(f"✅ Configuración cargada: {len(horarios)} horarios")
            
            return {
                'configuracion': config_general.to_dict(),
                'horarios': [h.to_dict() for h in horarios]
            }
            
        except Exception as e:
            print(f"❌ Error en obtener_configuracion_completa: {str(e)}")
            # Fallback para evitar errores en el frontend
            return {
                'configuracion': {
                    'nombre': 'Mi Barbería',
                    'telefono': '',
                    'email': '',
                    'direccion': '',
                    'duracion_turno': 60,
                    'intervalo_turnos': 30,
                    'max_turnos': 20
                },
                'horarios': []
            }
    
    # Método existente para solo guardar horarios (mantener compatibilidad)
    @staticmethod
    def guardar_horarios(horarios_data):
        try:
            for horario_data in horarios_data:
                horario = Negocio.query.filter_by(
                    dia_semana=horario_data['dia_semana']
                ).first()
                
                if not horario:
                    horario = Negocio()
                
                horario.dia_semana = horario_data['dia_semana']
                horario.abierto = horario_data.get('abierto', True)
                horario.hora_apertura = horario_data['hora_apertura']
                horario.hora_cierre = horario_data['hora_cierre']
                horario.hora_descanso_inicio = horario_data.get('hora_descanso_inicio')
                horario.hora_descanso_fin = horario_data.get('hora_descanso_fin')
                
                db.session.add(horario)
            
            db.session.commit()
            
            return {
                'success': True,
                'mensaje': 'Horarios guardados correctamente'
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'mensaje': f'Error al guardar horarios: {str(e)}'
            }