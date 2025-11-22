from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.auth.service import AuthService
from app.auth.models import Usuario
from datetime import timedelta

# Creamos un Blueprint para las rutas de auth
# Un Blueprint es como un "módulo de rutas" que después enchufamos en la app principal
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Ruta POST /api/auth/login
# Recibe nombre_usuario y contraseña en el body JSON
@auth_bp.route('/login', methods=['POST'])
def login():
    # Obtenemos los datos del request JSON
    data = request.get_json()
    
    # Validamos que lleguen ambos campos
    if not data or not data.get('nombre_usuario') or not data.get('contrasena'):
        return jsonify({'error': 'Falta nombre_usuario o contrasena'}), 400
    
    # Extraemos los valores
    nombre_usuario = data.get('nombre_usuario')
    contrasena = data.get('contrasena')
    
    # Llamamos al servicio para validar las credenciales
    resultado = AuthService.validar_credenciales(nombre_usuario, contrasena)
    
    # Si la validación falló, retornamos error
    if not resultado['success']:
        return jsonify({'error': resultado['mensaje']}), 401
    
    # Si llegamos acá, las credenciales son válidas
    # Extraemos el usuario del resultado
    usuario = resultado['usuario']
    
    # Generamos un JWT con el ID del usuario como identidad
    # El JWT expira en 24 horas (86400 segundos)
    access_token = create_access_token(
        identity=str(usuario.id),
        expires_delta=timedelta(hours=24)
    )
    
    # Imprimir el token generado (solo para debugging, quitar en producción)
    print(f'==========\nToken generado para usuario {usuario.nombre_usuario}: {access_token}\n==========')

    # Retornamos el token y info del usuario
    return jsonify({
        'success': True,
        'token': access_token,
        'usuario': usuario.to_dict()
    }), 200

# Ruta GET /api/auth/me (protegida con JWT)
# Esta ruta solo se puede acceder si el cliente envía un JWT válido
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def obtener_usuario_actual():
    usuario_id = get_jwt_identity()  # Esto ahora vendrá como string
    
    # Convertir a integer para buscar en la BD
    usuario = Usuario.query.get(int(usuario_id))
    
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    return jsonify({
        'usuario': usuario.to_dict()
    }), 200

# Ruta POST /api/auth/logout (opcional, para lógica de backend)
# En realidad, con JWT no necesitamos hacer nada en el servidor
# El logout se hace eliminando el token del cliente
# @auth_bp.route('/logout', methods=['POST'])
# @jwt_required()
# def logout():
#     return jsonify({'mensaje': 'Deslogueado correctamente'}), 200