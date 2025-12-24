# ============================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================

class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = 'tu_clave_secreta_super_segura_123'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''  # Cambiar por tu contraseña de MySQL
    MYSQL_DB = 'colegio_miguel_grau'
    MYSQL_CURSORCLASS = 'DictCursor'
    
    # Configuración de tokens JWT
    JWT_EXPIRATION_HOURS = 24
    
    # Configuración de la aplicación
    DEBUG = True
    PORT = 5000
