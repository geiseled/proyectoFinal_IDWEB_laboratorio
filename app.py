# ============================================
# APLICACIÓN PRINCIPAL - MODULAR
# Sistema de Gestión Educativa - Colegio Miguel Grau
# ============================================

from flask import Flask, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
from datetime import datetime

# Importar configuración
from backend.config import Config

# Importar funciones de inicialización de rutas
from backend.auth_routes import init_auth_routes, auth_bp
from backend.tareas_routes import init_tareas_routes, tareas_bp
from backend.calificaciones_routes import init_calificaciones_routes, calificaciones_bp

# ============================================
# INICIALIZACIÓN DE LA APLICACIÓN
# ============================================

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar extensiones
CORS(app)  # Permitir peticiones desde el frontend
mysql = MySQL(app)

# ============================================
# REGISTRO DE BLUEPRINTS (RUTAS MODULARES)
# ============================================

# Inicializar rutas con sus dependencias
auth_blueprint = init_auth_routes(mysql, app)
tareas_blueprint = init_tareas_routes(mysql, app)
calificaciones_blueprint = init_calificaciones_routes(mysql, app)

# Registrar blueprints con sus prefijos
app.register_blueprint(auth_blueprint, url_prefix='/api')
app.register_blueprint(tareas_blueprint, url_prefix='/api/tareas')
app.register_blueprint(calificaciones_blueprint, url_prefix='/api/calificaciones')

# ============================================
# RUTA DE SALUD
# ============================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica que el servidor esté funcionando"""
    try:
        # Verificar conexión a la base de datos
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        cur.close()
        db_status = "OK"
    except:
        db_status = "ERROR"
    
    return jsonify({
        'status': 'OK',
        'mensaje': 'Servidor funcionando correctamente',
        'database': db_status,
        'timestamp': datetime.now().isoformat()
    }), 200

# ============================================
# MANEJO DE ERRORES
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'exito': False,
        'mensaje': 'Ruta no encontrada'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'exito': False,
        'mensaje': 'Error interno del servidor'
    }), 500

# ============================================
# INICIAR SERVIDOR
# ============================================

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Iniciando servidor del Colegio Miguel Grau")
    print("=" * 60)
    print(f"📍 URL: http://localhost:{Config.PORT}")
    print(f"🔧 Modo: {'Desarrollo' if Config.DEBUG else 'Producción'}")
    print("=" * 60)
    app.run(debug=Config.DEBUG, port=Config.PORT)
