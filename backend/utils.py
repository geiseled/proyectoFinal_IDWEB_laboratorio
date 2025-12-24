# ============================================
# UTILIDADES Y VALIDACIONES
# ============================================

import re
from datetime import datetime, timedelta
import jwt

def validar_dni(dni):
    """Valida que el DNI tenga 8 dígitos"""
    return bool(re.match(r'^\d{8}$', dni))

def validar_correo(correo):
    """Valida que sea un correo de Gmail"""
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@gmail\.com$', correo))

def validar_contrasena(contrasena):
    """Valida que la contraseña tenga al menos 6 caracteres y un número"""
    if len(contrasena) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres"
    if not any(char.isdigit() for char in contrasena):
        return False, "La contraseña debe contener al menos un número"
    return True, "OK"

def generar_token(usuario_id, tipo, secret_key, expiration_hours=24):
    """Genera un JWT token"""
    payload = {
        'usuario_id': usuario_id,
        'tipo': tipo,
        'exp': datetime.utcnow() + timedelta(hours=expiration_hours)
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

def verificar_token(token, secret_key):
    """Verifica y decodifica el token"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
