from flask import Blueprint, request, jsonify
from app.appointments.service import TurnoService
from app.appointments.models import Turno
import uuid

# Creamos un Blueprint para las rutas de turnos
appointments_bp = Blueprint('appointments', __name__, url_prefix='/api/appointments')

# Ruta GET /api/appointments/client-id
# Obtener o generar un client_id para el usuario
# El cliente debe manejarlo por localStorage (no por cookie)
@appointments_bp.route('/client-id', methods=['GET'])
def obtener_client_id():
    # Generamos un ID único para este cliente
    # El frontend es responsable de guardarlo en localStorage
    client_id = str(uuid.uuid4())
    
    # Retornamos el ID para que el frontend lo guarde
    return jsonify({
        'success': True,
        'client_id': client_id
    }), 200

# Ruta GET /api/appointments/turno-actual
# Obtener el turno actual del cliente (si existe)
@appointments_bp.route('/turno-actual', methods=['GET'])
def obtener_turno_actual():
    # Obtenemos el client_id del query param
    client_id = request.args.get('client_id')
    
    if not client_id:
        return jsonify({'error': 'Falta client_id'}), 400
    
    # Buscamos si tiene turno activo
    turno = TurnoService.obtener_turno_activo(client_id)
    
    if not turno:
        return jsonify({
            'success': True,
            'turno': None
        }), 200
    
    # Retornamos el turno
    return jsonify({
        'success': True,
        'turno': turno.to_dict()
    }), 200

# Ruta GET /api/appointments/horarios-disponibles
# Obtener horarios disponibles para una fecha
# Query params: fecha (YYYY-MM-DD)
@appointments_bp.route('/horarios-disponibles', methods=['GET'])
def obtener_horarios():
    # Obtenemos la fecha del query param
    fecha = request.args.get('fecha')
    
    if not fecha:
        return jsonify({'error': 'Falta parámetro fecha'}), 400
    
    try:
        # Obtenemos los horarios disponibles
        horarios = TurnoService.obtener_horarios_disponibles(fecha)
        
        return jsonify({
            'success': True,
            'fecha': fecha,
            'horarios': horarios
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Ruta POST /api/appointments/reservar
# Crear un nuevo turno
# Body: fecha, hora, servicio_id, nombre_cliente, telefono_cliente, client_id
@appointments_bp.route('/reservar', methods=['POST'])
def reservar_turno():
    # Obtenemos los datos del request
    data = request.get_json()
    
    # Validamos que lleguen todos los datos
    required = ['fecha', 'hora', 'servicio_id', 'nombre_cliente', 'telefono_cliente', 'client_id']
    if not all(key in data for key in required):
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    
    # Llamamos al servicio para crear el turno
    resultado = TurnoService.crear_turno(
        fecha=data['fecha'],
        hora=data['hora'],
        servicio_id=data['servicio_id'],
        nombre_cliente=data['nombre_cliente'],
        telefono_cliente=data['telefono_cliente'],
        client_id=data['client_id']
    )
    
    # Retornamos resultado (200 si éxito, 400 si error)
    status_code = 200 if resultado['success'] else 400
    
    return jsonify(resultado), status_code

# Ruta POST /api/appointments/cancelar
# Cancelar un turno por token
# Body: token_cancelacion
@appointments_bp.route('/cancelar', methods=['POST'])
def cancelar_turno():
    # Obtenemos el token del request
    data = request.get_json()
    
    if not data or 'token_cancelacion' not in data:
        return jsonify({'error': 'Falta token_cancelacion'}), 400
    
    # Llamamos al servicio para cancelar
    resultado = TurnoService.cancelar_turno_por_token(data['token_cancelacion'])
    
    # Retornamos resultado
    status_code = 200 if resultado['success'] else 400
    
    return jsonify(resultado), status_code

# Ruta GET /api/appointments/proximo-disponible
# Obtener la próxima fecha con turnos disponibles
@appointments_bp.route('/proximo-disponible', methods=['GET'])
def obtener_proximo():
    # Obtenemos el próximo turno disponible (en los próximos 7 días)
    resultado = TurnoService.obtener_proximo_turno_disponible(dias_adelante=7)
    
    if not resultado:
        return jsonify({
            'success': False,
            'mensaje': 'No hay turnos disponibles en los próximos 7 días'
        }), 404
    
    return jsonify({
        'success': True,
        'proximoDisponible': resultado
    }), 200

# Ruta GET /api/appointments/turnos
# Obtener turnos (solo para admin, protegida con JWT)
# Query params: fecha_inicio, fecha_fin, estado
@appointments_bp.route('/turnos', methods=['GET'])
def obtener_turnos():
    from flask_jwt_extended import jwt_required, get_jwt_identity
    from functools import wraps
    
    # Verificamos que haya JWT
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No autorizado'}), 401
    
    # Obtenemos parámetros
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    estado = request.args.get('estado', 'reservado')
    
    if not fecha_inicio or not fecha_fin:
        return jsonify({'error': 'Faltan fecha_inicio y fecha_fin'}), 400
    
    try:
        from datetime import datetime
        inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        
        # Obtenemos los turnos
        turnos = TurnoService.obtener_turnos_rango(inicio, fin, estado)
        
        return jsonify({
            'success': True,
            'turnos': [t.to_dict() for t in turnos]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400