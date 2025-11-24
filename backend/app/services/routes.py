from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.service import ServicioService

# Blueprint para servicios
servicios_bp = Blueprint('servicios', __name__, url_prefix='/api/servicios')

# Obtener todos los servicios
@servicios_bp.route('/', methods=['GET'])
@jwt_required()
def obtener_servicios():
    servicios = ServicioService.obtener_todos_servicios()
    servicios_dict = [s.to_dict() for s in servicios]
    return jsonify({
        'success': True,
        'servicios': servicios_dict
    }), 200

# Crear nuevo servicio
@servicios_bp.route('/', methods=['POST'])
@jwt_required()
def crear_servicio():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'mensaje': 'Falta información del servicio'}), 400
    
    resultado = ServicioService.crear_servicio(data)
    status_code = 200 if resultado['success'] else 400
    return jsonify(resultado), status_code

# Actualizar servicio
@servicios_bp.route('/<int:servicio_id>', methods=['PUT'])
@jwt_required()
def actualizar_servicio(servicio_id):
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'mensaje': 'Falta información del servicio'}), 400
    
    resultado = ServicioService.actualizar_servicio(servicio_id, data)
    status_code = 200 if resultado['success'] else 400
    return jsonify(resultado), status_code

# Eliminar servicio
@servicios_bp.route('/<int:servicio_id>', methods=['DELETE'])
@jwt_required()
def eliminar_servicio(servicio_id):
    resultado = ServicioService.eliminar_servicio(servicio_id)
    status_code = 200 if resultado['success'] else 400
    return jsonify(resultado), status_code

# Guardar múltiples servicios
@servicios_bp.route('/guardar-multiples', methods=['POST'])
@jwt_required()
def guardar_servicios():
    data = request.get_json()
    if not data or 'servicios' not in data:
        return jsonify({'success': False, 'mensaje': 'Falta información de servicios'}), 400
    
    resultado = ServicioService.guardar_servicios(data['servicios'])
    status_code = 200 if resultado['success'] else 400
    return jsonify(resultado), status_code