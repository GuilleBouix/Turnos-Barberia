from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.management.service import GestionTurnosService

# Creamos un Blueprint para las rutas de gestión de turnos
management_bp = Blueprint('management', __name__, url_prefix='/api/management')

# Obtener todos los turnos (con filtro opcional por fecha)
@management_bp.route('/turnos', methods=['GET'])
@jwt_required()
def obtener_turnos():
    fecha_filtro = request.args.get('fecha')
    
    turnos = GestionTurnosService.obtener_todos_turnos(fecha_filtro)
    turnos_dict = [t.to_dict() for t in turnos]
    
    return jsonify({
        'success': True,
        'turnos': turnos_dict,
        'total': len(turnos_dict)
    }), 200

# Obtener turnos de hoy
@management_bp.route('/turnos/hoy', methods=['GET'])
@jwt_required()
def obtener_turnos_hoy():
    turnos = GestionTurnosService.obtener_turnos_hoy()
    turnos_dict = [t.to_dict() for t in turnos]
    
    return jsonify({
        'success': True,
        'turnos': turnos_dict,
        'total': len(turnos_dict)
    }), 200

# Marcar turno como completado
@management_bp.route('/turnos/<int:turno_id>/completar', methods=['PUT'])
@jwt_required()
def completar_turno(turno_id):
    resultado = GestionTurnosService.marcar_como_completado(turno_id)
    status_code = 200 if resultado['success'] else 400
    return jsonify(resultado), status_code

# Eliminar turno
@management_bp.route('/turnos/<int:turno_id>', methods=['DELETE'])
@jwt_required()
def eliminar_turno(turno_id):
    resultado = GestionTurnosService.eliminar_turno(turno_id)
    status_code = 200 if resultado['success'] else 400
    return jsonify(resultado), status_code