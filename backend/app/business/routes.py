from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.business.service import NegocioService

# Creamos un Blueprint para las rutas de negocio
business_bp = Blueprint('business', __name__, url_prefix='/api/business')

# Ruta GET /api/business/config
# Obtener configuración general del negocio
@business_bp.route('/config', methods=['GET'])
def obtener_configuracion():
    # Llamamos al servicio para obtener la configuración
    config = NegocioService.obtener_configuracion()
    
    if not config:
        return jsonify({
            'success': False,
            'mensaje': 'No hay configuración'
        }), 404
    
    # Retornamos la configuración
    return jsonify({
        'success': True,
        'configuracion': config
    }), 200

# Ruta GET /api/business/horarios
# Obtener todos los horarios de la semana
@business_bp.route('/horarios', methods=['GET'])
def obtener_horarios():
    # Llamamos al servicio para obtener todos los horarios
    horarios = NegocioService.obtener_todos_horarios()
    
    # Convertimos a lista de dicts
    horarios_dict = [h.to_dict() for h in horarios]
    
    # Retornamos los horarios
    return jsonify({
        'success': True,
        'horarios': horarios_dict
    }), 200

# Ruta POST /api/business/config
# Guardar configuración completa (general + horarios)
# Body: nombre, telefono, email, direccion, duracion_turno, intervalo_turnos, max_turnos, horarios
@business_bp.route('/config', methods=['POST'])
@jwt_required()
def guardar_configuracion():
    # Obtenemos los datos del request
    data = request.get_json()
    
    # Validamos que llegue información mínima
    if not data:
        return jsonify({'error': 'Falta información'}), 400
    
    # Llamamos al servicio para guardar
    resultado = NegocioService.guardar_configuracion_completa(data)
    
    # Retornamos resultado
    status_code = 200 if resultado['success'] else 400
    
    return jsonify(resultado), status_code

# Ruta GET /api/business/horarios/<int:dia_semana>
# Obtener horario de un día específico
@business_bp.route('/horarios/<int:dia_semana>', methods=['GET'])
def obtener_horario_dia(dia_semana):
    # Validamos que el día esté entre 0 y 6
    if dia_semana < 0 or dia_semana > 6:
        return jsonify({'error': 'Día inválido (debe ser 0-6)'}), 400
    
    # Buscamos el horario para ese día
    horario = NegocioService.obtener_horario_por_dia(dia_semana)
    
    # Si no existe, retornamos 404
    if not horario:
        return jsonify({'error': 'No hay horario para ese día'}), 404
    
    # Retornamos el horario
    return jsonify({
        'success': True,
        'horario': horario.to_dict()
    }), 200

# Ruta GET /api/business/abierto-hoy
# Verificar si el negocio está abierto hoy
@business_bp.route('/abierto-hoy', methods=['GET'])
def esta_abierto_hoy():
    # Verificamos si está abierto
    abierto = NegocioService.esta_abierto_hoy()
    
    # Retornamos el estado
    return jsonify({
        'success': True,
        'abierto': abierto
    }), 200