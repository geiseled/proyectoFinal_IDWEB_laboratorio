# ============================================
# RUTAS DE AUTENTICACIÓN
# ============================================

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from backend.utils import (
    validar_dni, validar_correo, validar_contrasena, 
    generar_token
)

auth_bp = Blueprint('auth', __name__)

def init_auth_routes(mysql, app):
    """Inicializa las rutas de autenticación con las dependencias necesarias"""
    
    @auth_bp.route('/registro/profesor', methods=['POST'])
    def registro_profesor():
        """Registra un nuevo profesor"""
        try:
            datos = request.get_json()
            
            # Validaciones
            if not validar_dni(datos['dni']):
                return jsonify({'exito': False, 'mensaje': 'DNI inválido'}), 400
            
            if not validar_correo(datos['correo']):
                return jsonify({'exito': False, 'mensaje': 'Correo debe ser de Gmail'}), 400
            
            valido, mensaje = validar_contrasena(datos['contrasena'])
            if not valido:
                return jsonify({'exito': False, 'mensaje': mensaje}), 400
            
            # Verificar ID único
            cur = mysql.connection.cursor()
            cur.execute("SELECT id FROM usuarios WHERE id = %s", (datos['id'],))
            if cur.fetchone():
                return jsonify({'exito': False, 'mensaje': 'Este ID ya está registrado'}), 400
            
            # Verificar correo único
            cur.execute("SELECT correo FROM usuarios WHERE correo = %s", (datos['correo'],))
            if cur.fetchone():
                return jsonify({'exito': False, 'mensaje': 'Este correo ya está registrado'}), 400
            
            # Hash de la contraseña
            hash_contrasena = generate_password_hash(datos['contrasena'])
            
            # Insertar usuario
            cur.execute("""
                INSERT INTO usuarios (id, nombres, apellidos, dni, correo, contrasena, tipo)
                VALUES (%s, %s, %s, %s, %s, %s, 'profesor')
            """, (datos['id'], datos['nombres'], datos['apellidos'], 
                datos['dni'], datos['correo'], hash_contrasena))
            
            # Insertar en tabla profesores
            cur.execute("""
                INSERT INTO profesores (usuario_id, especialidad)
                VALUES (%s, %s)
            """, (datos['id'], datos.get('especialidad', '')))
            
            mysql.connection.commit()
            cur.close()
            
            return jsonify({
                'exito': True,
                'mensaje': 'Registro exitoso. Ahora puedes iniciar sesión.'
            }), 201
            
        except Exception as e:
            print(f"Error en registro_profesor: {e}")
            return jsonify({'exito': False, 'mensaje': 'Error en el servidor'}), 500

    @auth_bp.route('/registro/estudiante', methods=['POST'])
    def registro_estudiante():
        """Registra un nuevo estudiante"""
        try:
            datos = request.get_json()
            
            # Validaciones
            if not validar_dni(datos['dni']):
                return jsonify({'exito': False, 'mensaje': 'DNI inválido'}), 400
            
            if not validar_correo(datos['correo']):
                return jsonify({'exito': False, 'mensaje': 'Correo debe ser de Gmail'}), 400
            
            valido, mensaje = validar_contrasena(datos['contrasena'])
            if not valido:
                return jsonify({'exito': False, 'mensaje': mensaje}), 400
            
            # Verificar ID y correo únicos
            cur = mysql.connection.cursor()
            cur.execute("SELECT id FROM usuarios WHERE id = %s OR correo = %s", 
                    (datos['id'], datos['correo']))
            if cur.fetchone():
                return jsonify({'exito': False, 'mensaje': 'ID o correo ya registrado'}), 400
            
            # Hash de la contraseña
            hash_contrasena = generate_password_hash(datos['contrasena'])
            
            # Insertar usuario
            cur.execute("""
                INSERT INTO usuarios (id, nombres, apellidos, dni, correo, contrasena, tipo)
                VALUES (%s, %s, %s, %s, %s, %s, 'estudiante')
            """, (datos['id'], datos['nombres'], datos['apellidos'], 
                datos['dni'], datos['correo'], hash_contrasena))
            
            # Insertar en tabla estudiantes
            cur.execute("""
                INSERT INTO estudiantes (usuario_id, grado, seccion)
                VALUES (%s, %s, %s)
            """, (datos['id'], datos.get('grado', ''), datos.get('seccion', '')))
            
            mysql.connection.commit()
            cur.close()
            
            return jsonify({
                'exito': True,
                'mensaje': 'Registro exitoso. Ahora puedes iniciar sesión.'
            }), 201
            
        except Exception as e:
            print(f"Error en registro_estudiante: {e}")
            return jsonify({'exito': False, 'mensaje': 'Error en el servidor'}), 500

    @auth_bp.route('/login', methods=['POST'])
    def login():
        """Inicia sesión y devuelve un token"""
        try:
            datos = request.get_json()
            
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT id, nombres, apellidos, correo, contrasena, tipo, fecha_registro
                FROM usuarios WHERE id = %s
            """, (datos['id'],))
            
            usuario = cur.fetchone()
            cur.close()
            
            if not usuario:
                return jsonify({'exito': False, 'mensaje': 'Usuario no encontrado'}), 404
            
            # Verificar contraseña
            if not check_password_hash(usuario['contrasena'], datos['contrasena']):
                return jsonify({'exito': False, 'mensaje': 'Contraseña incorrecta'}), 401
            
            # Generar token
            token = generar_token(usuario['id'], usuario['tipo'], app.config['SECRET_KEY'])
            
            # Actualizar último acceso
            cur = mysql.connection.cursor()
            cur.execute("UPDATE usuarios SET ultimo_acceso = NOW() WHERE id = %s", (usuario['id'],))
            mysql.connection.commit()
            cur.close()
            
            return jsonify({
                'exito': True,
                'token': token,
                'usuario': {
                    'id': usuario['id'],
                    'nombres': usuario['nombres'],
                    'apellidos': usuario['apellidos'],
                    'correo': usuario['correo'],
                    'tipo': usuario['tipo']
                },
                'mensaje': f"Bienvenido, {usuario['nombres']}!"
            }), 200
            
        except Exception as e:
            print(f"Error en login: {e}")
            return jsonify({'exito': False, 'mensaje': 'Error en el servidor'}), 500
    
    return auth_bp
