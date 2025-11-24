from app.services.models import Servicio
from app.database import db
from datetime import datetime, time, timedelta

class ServicioService:
    
    @staticmethod
    def obtener_todos_servicios():
        """Obtener todos los servicios ordenados por categoría y nombre"""
        try:
            servicios = Servicio.query.order_by(Servicio.categoria, Servicio.nombre_servicio).all()
            return servicios
        except Exception as e:
            print(f"Error al obtener servicios: {str(e)}")
            return []
    
    @staticmethod
    def obtener_servicio_por_id(servicio_id):
        """Obtener un servicio por su ID"""
        try:
            servicio = Servicio.query.get(servicio_id)
            return servicio
        except Exception as e:
            print(f"Error al obtener servicio: {str(e)}")
            return None
    
    @staticmethod
    def crear_servicio(datos):
        """Crear un nuevo servicio"""
        try:
            servicio = Servicio(
                nombre_servicio=datos['nombre_servicio'],
                categoria=datos['categoria'],
                precio=datos['precio'],
                activo=datos.get('activo', True)
            )
            db.session.add(servicio)
            db.session.commit()
            return {'success': True, 'servicio': servicio.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'mensaje': f'Error al crear servicio: {str(e)}'}
    
    @staticmethod
    def actualizar_servicio(servicio_id, datos):
        """Actualizar un servicio existente"""
        try:
            servicio = Servicio.query.get(servicio_id)
            if not servicio:
                return {'success': False, 'mensaje': 'Servicio no encontrado'}
            
            servicio.nombre_servicio = datos.get('nombre_servicio', servicio.nombre_servicio)
            servicio.categoria = datos.get('categoria', servicio.categoria)
            servicio.precio = datos.get('precio', servicio.precio)
            servicio.activo = datos.get('activo', servicio.activo)
            
            db.session.commit()
            return {'success': True, 'servicio': servicio.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'mensaje': f'Error al actualizar servicio: {str(e)}'}
    
    @staticmethod
    def eliminar_servicio(servicio_id):
        """Eliminar un servicio"""
        try:
            servicio = Servicio.query.get(servicio_id)
            if not servicio:
                return {'success': False, 'mensaje': 'Servicio no encontrado'}
            
            db.session.delete(servicio)
            db.session.commit()
            return {'success': True, 'mensaje': 'Servicio eliminado correctamente'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'mensaje': f'Error al eliminar servicio: {str(e)}'}
    
    @staticmethod
    def guardar_servicios(servicios_data):
        """Guardar/actualizar múltiples servicios"""
        try:
            for servicio_data in servicios_data:
                if servicio_data.get('id'):
                    # Actualizar servicio existente
                    servicio = Servicio.query.get(servicio_data['id'])
                    if servicio:
                        servicio.nombre_servicio = servicio_data['nombre_servicio']
                        servicio.categoria = servicio_data['categoria']
                        servicio.precio = servicio_data['precio']
                        servicio.activo = servicio_data.get('activo', True)
                else:
                    # Crear nuevo servicio
                    servicio = Servicio(
                        nombre_servicio=servicio_data['nombre_servicio'],
                        categoria=servicio_data['categoria'],
                        precio=servicio_data['precio'],
                        activo=servicio_data.get('activo', True)
                    )
                    db.session.add(servicio)
            
            db.session.commit()
            return {'success': True, 'mensaje': 'Servicios guardados correctamente'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'mensaje': f'Error al guardar servicios: {str(e)}'}