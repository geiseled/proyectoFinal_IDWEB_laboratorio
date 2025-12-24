# ============================================
# RUTAS DE TAREAS (PROFESORES)
# ============================================

from flask import Blueprint, request, jsonify
from backend.utils import verificar_token

tareas_bp = Blueprint('tareas', __name__)

def init_tareas_routes(mysql, app):
    """Inicializa las rutas de tareas con las dependencias necesarias"""
    
    @tareas_bp.route('', methods=['POST'])
    def crear_tarea():
        """Crea una nueva tarea"""
        try:
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'exito': False, 'mensaje': 'Token requerido'}), 401
            
            payload = verificar_token(token.replace('Bearer ', ''), app.config['SECRET_KEY'])
            if not payload or payload['tipo'] != 'profesor':
                return jsonify({'exito': False, 'mensaje': 'No autorizado'}), 403
            
            datos = request.get_json()
            
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO tareas (titulo, descripcion, curso, tipo, fecha_entrega, 
                                puntos, profesor_id, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'activa')
            """, (datos['titulo'], datos['descripcion'], datos['curso'],
                datos.get('tipo', 'tarea'), datos['fechaEntrega'], 
                datos.get('puntos', 20), payload['usuario_id']))
            
            mysql.connection.commit()
            tarea_id = cur.lastrowid
            cur.close()
            
            return jsonify({
                'exito': True,
                'tarea_id': tarea_id,
                'mensaje': 'Tarea creada exitosamente'
            }), 201
            
        except Exception as e:
            print(f"Error en crear_tarea: {e}")
            return jsonify({'exito': False, 'mensaje': 'Error en el servidor'}), 500

    @tareas_bp.route('/profesor', methods=['GET'])
    def obtener_tareas_profesor():
        """Obtiene todas las tareas de un profesor"""
        try:
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'exito': False, 'mensaje': 'Token requerido'}), 401
            
            payload = verificar_token(token.replace('Bearer ', ''), app.config['SECRET_KEY'])
            if not payload:
                return jsonify({'exito': False, 'mensaje': 'Token inválido'}), 401
            
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT t.*, 
                    COUNT(e.id) as total_entregas,
                    COUNT(CASE WHEN e.nota IS NOT NULL THEN 1 END) as calificadas
                FROM tareas t
                LEFT JOIN entregas e ON t.id = e.tarea_id
                WHERE t.profesor_id = %s
                GROUP BY t.id
                ORDER BY t.fecha_creacion DESC
            """, (payload['usuario_id'],))
            
            tareas = cur.fetchall()
            cur.close()
            
            return jsonify({'exito': True, 'tareas': tareas}), 200
            
        except Exception as e:
            print(f"Error en obtener_tareas_profesor: {e}")
            return jsonify({'exito': False, 'mensaje': 'Error en el servidor'}), 500

    @tareas_bp.route('/<int:tarea_id>', methods=['DELETE'])
    def eliminar_tarea(tarea_id):
        """Elimina una tarea"""
        try:
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'exito': False, 'mensaje': 'Token requerido'}), 401
            
            payload = verificar_token(token.replace('Bearer ', ''), app.config['SECRET_KEY'])
            if not payload or payload['tipo'] != 'profesor':
                return jsonify({'exito': False, 'mensaje': 'No autorizado'}), 403
            
            cur = mysql.connection.cursor()
            
            # Verificar que la tarea pertenece al profesor
            cur.execute("SELECT profesor_id FROM tareas WHERE id = %s", (tarea_id,))
            tarea = cur.fetchone()
            
            if not tarea or tarea['profesor_id'] != payload['usuario_id']:
                return jsonify({'exito': False, 'mensaje': 'Tarea no encontrada'}), 404
            
            # Eliminar tarea
            cur.execute("DELETE FROM tareas WHERE id = %s", (tarea_id,))
            mysql.connection.commit()
            cur.close()
            
            return jsonify({'exito': True, 'mensaje': 'Tarea eliminada'}), 200
            
        except Exception as e:
            print(f"Error en eliminar_tarea: {e}")
            return jsonify({'exito': False, 'mensaje': 'Error en el servidor'}), 500
    
    @tareas_bp.route('/estudiante', methods=['GET'])
    def obtener_tareas_estudiante():
        """Obtiene todas las tareas para un estudiante"""
        try:
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'exito': False, 'mensaje': 'Token requerido'}), 401
            
            payload = verificar_token(token.replace('Bearer ', ''), app.config['SECRET_KEY'])
            if not payload:
                return jsonify({'exito': False, 'mensaje': 'Token inválido'}), 401
            
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT t.*, 
                    u.nombres as profesor_nombres, 
                    u.apellidos as profesor_apellidos,
                    e.nota, e.comentario, e.estado as estado_entrega,
                    DATEDIFF(t.fecha_entrega, CURDATE()) as dias_restantes
                FROM tareas t
                LEFT JOIN usuarios u ON t.profesor_id = u.id
                LEFT JOIN entregas e ON t.id = e.tarea_id AND e.estudiante_id = %s
                ORDER BY t.fecha_entrega ASC
            """, (payload['usuario_id'],))
            
            tareas = cur.fetchall()
            cur.close()
            
            return jsonify({'exito': True, 'tareas': tareas}), 200
            
        except Exception as e:
            print(f"Error en obtener_tareas_estudiante: {e}")
            return jsonify({'exito': False, 'mensaje': 'Error en el servidor'}), 500
    
    return tareas_bp
