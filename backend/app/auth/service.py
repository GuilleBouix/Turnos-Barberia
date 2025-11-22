from app.auth.models import Usuario
from app.database import db

# Servicio de autenticación: centraliza la lógica de login
# Esto lo hacemos así para no mezclar la lógica con las rutas
class AuthService:
    # Método para buscar un usuario por nombre_usuario
    # Retorna el objeto Usuario si existe, None si no
    @staticmethod
    def buscar_usuario_por_nombre(nombre_usuario):
        # Consultamos la BD: "SELECT * FROM usuarios WHERE nombre_usuario = ?"
        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        return usuario

    # Método para validar credenciales (nombre + contrasena)
    # Retorna un diccionario con success (True/False) y el usuario si es exitoso
    @staticmethod
    def validar_credenciales(nombre_usuario, contrasena):
        # Buscamos el usuario en la BD
        usuario = AuthService.buscar_usuario_por_nombre(nombre_usuario)
        
        # Si no existe, retornamos error
        if not usuario:
            return {
                'success': False,
                'mensaje': 'Usuario o contraseña incorrectos.',
                'usuario': None
            }
        
        # Si existe, verificamos que la contrasena sea correcta
        # Usamos el método verificar_contrasena() del modelo
        if not usuario.verificar_contrasena(contrasena):
            return {
                'success': False,
                'mensaje': 'contrasena incorrecta',
                'usuario': None
            }
        
        # Si llegamos acá, todo está bien
        return {
            'success': True,
            'mensaje': 'Credenciales válidas',
            'usuario': usuario
        }