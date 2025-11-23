from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.business.service import NegocioService

business_bp = Blueprint('business', __name__, url_prefix='/api/business')

# Ruta para obtener toda la configuración (general + horarios)
@business_bp.route('/config', methods=['GET'])
@jwt_required()
def obtener_configuracion_completa():
    try:
        config_completa = NegocioService.obtener_configuracion_completa()
        return jsonify({
            'success': True,
            **config_completa
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'mensaje': f'Error al obtener configuración: {str(e)}'
        }), 500

# Ruta para guardar toda la configuración
@business_bp.route('/config', methods=['POST'])
@jwt_required()
def guardar_configuracion_completa():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Falta información de configuración'}), 400
    
    resultado = NegocioService.guardar_configuracion_completa(data)
    status_code = 200 if resultado['success'] else 400
    return jsonify(resultado), status_code

# Rutas existentes (mantener para compatibilidad)
@business_bp.route('/horarios', methods=['GET'])
@jwt_required()
def obtener_horarios():
    horarios = NegocioService.obtener_todos_horarios()
    horarios_dict = [h.to_dict() for h in horarios]
    return jsonify({
        'success': True,
        'horarios': horarios_dict
    }), 200

@business_bp.route('/horarios', methods=['POST'])
@jwt_required()
def guardar_horarios():
    data = request.get_json()
    if not data or 'horarios' not in data:
        return jsonify({'error': 'Falta información de horarios'}), 400
    
    resultado = NegocioService.guardar_horarios(data['horarios'])
    status_code = 200 if resultado['success'] else 400
    return jsonify(resultado), status_code

@business_bp.route('/horarios/<int:dia_semana>', methods=['GET'])
@jwt_required()
def obtener_horario_dia(dia_semana):
    if dia_semana < 0 or dia_semana > 6:
        return jsonify({'error': 'Día inválido (debe ser 0-6)'}), 400
    
    horario = NegocioService.obtener_horario_por_dia(dia_semana)
    if not horario:
        return jsonify({'error': 'No hay horario para ese día'}), 404
    
    return jsonify({
        'success': True,
        'horario': horario.to_dict()
    }), 200

@business_bp.route('/horarios-disponibles/<int:dia_semana>', methods=['GET'])
def obtener_slots_disponibles(dia_semana):
    if dia_semana < 0 or dia_semana > 6:
        return jsonify({'error': 'Día inválido (debe ser 0-6)'}), 400
    
    slots = NegocioService.obtener_horarios_disponibles(dia_semana, duracion_turno=60)
    return jsonify({
        'success': True,
        'slots': slots,
        'dia_semana': dia_semana
    }), 200

@business_bp.route('/abierto-hoy', methods=['GET'])
def esta_abierto_hoy():
    abierto = NegocioService.esta_abierto_hoy()
    return jsonify({
        'success': True,
        'abierto': abierto
    }), 200