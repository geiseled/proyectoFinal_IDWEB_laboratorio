# ============================================
# RUTAS DE CALIFICACIONES (PROFESORES)
# ============================================

from flask import Blueprint, request, jsonify
from backend.utils import verificar_token

calificaciones_bp = Blueprint('calificaciones', __name__)

def init_calificaciones_routes(mysql, app):
    """Inicializa las rutas de calificaciones con las dependencias necesarias"""
    
    @calificaciones_bp.route('', methods=['POST'])
    def asignar_calificacion():
        """Asigna o actualiza una calificación"""
        try:
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'exito': False, 'mensaje': 'Token requerido'}), 401
            
            payload = verificar_token(token.replace('Bearer ', ''), app.config['SECRET_KEY'])
            if not payload or payload['tipo'] != 'profesor':
                return jsonify({'exito': False, 'mensaje': 'No autorizado'}), 403
            
            datos = request.get_json()
            
            # Validar nota
            nota = float(datos['nota'])
            if nota < 0 or nota > 20:
                return jsonify({'exito': False, 'mensaje': 'Nota debe estar entre 0 y 20'}), 400
            
            cur = mysql.connection.cursor()
            
            # Verificar si ya existe una entrega
            cur.execute("""
                SELECT id FROM entregas 
                WHERE tarea_id = %s AND estudiante_id = %s
            """, (datos['tarea_id'], datos['estudiante_id']))
            
            entrega = cur.fetchone()
            
            if entrega:
                # Actualizar entrega existente
                cur.execute("""
                    UPDATE entregas 
                    SET nota = %s, comentario = %s, estado = 'calificada',
                        fecha_calificacion = NOW()
                    WHERE id = %s
                """, (nota, datos.get('comentario', ''), entrega['id']))
            else:
                # Crear nueva entrega
                cur.execute("""
                    INSERT INTO entregas (tarea_id, estudiante_id, nota, comentario, 
                                        estado, fecha_calificacion)
                    VALUES (%s, %s, %s, %s, 'calificada', NOW())
                """, (datos['tarea_id'], datos['estudiante_id'], 
                    nota, datos.get('comentario', '')))
            
            mysql.connection.commit()
            cur.close()
            
            return jsonify({
                'exito': True,
                'mensaje': 'Calificación asignada exitosamente'
            }), 200
            
        except Exception as e:
            print(f"Error en asignar_calificacion: {e}")
            return jsonify({'exito': False, 'mensaje': 'Error en el servidor'}), 500

    @calificaciones_bp.route('/tarea/<int:tarea_id>/entregas', methods=['GET'])
    def obtener_entregas(tarea_id):
        """Obtiene todas las entregas de una tarea"""
        try:
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'exito': False, 'mensaje': 'Token requerido'}), 401
            
            payload = verificar_token(token.replace('Bearer ', ''), app.config['SECRET_KEY'])
            if not payload:
                return jsonify({'exito': False, 'mensaje': 'Token inválido'}), 401
            
            cur = mysql.connection.cursor()
            
            # Obtener todos los estudiantes y sus entregas
            cur.execute("""
                SELECT u.id, u.nombres, u.apellidos,
                    e.nota, e.comentario, e.fecha_calificacion, e.estado
                FROM usuarios u
                LEFT JOIN entregas e ON u.id = e.estudiante_id AND e.tarea_id = %s
                WHERE u.tipo = 'estudiante'
                ORDER BY u.apellidos, u.nombres
            """, (tarea_id,))
            
            entregas = cur.fetchall()
            cur.close()
            
            return jsonify({'exito': True, 'entregas': entregas}), 200
            
        except Exception as e:
            print(f"Error en obtener_entregas: {e}")
            return jsonify({'exito': False, 'mensaje': 'Error en el servidor'}), 500

    @calificaciones_bp.route('/estudiante/estadisticas', methods=['GET'])
    def obtener_estadisticas_estudiante():
        """Obtiene estadísticas del estudiante"""
        try:
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'exito': False, 'mensaje': 'Token requerido'}), 401
            
            payload = verificar_token(token.replace('Bearer ', ''), app.config['SECRET_KEY'])
            if not payload:
                return jsonify({'exito': False, 'mensaje': 'Token inválido'}), 401
            
            cur = mysql.connection.cursor()
            
            # Total de tareas
            cur.execute("SELECT COUNT(*) as total FROM tareas")
            total_tareas = cur.fetchone()['total']
            
            # Tareas calificadas
            cur.execute("""
                SELECT COUNT(*) as calificadas, AVG(nota) as promedio
                FROM entregas 
                WHERE estudiante_id = %s AND nota IS NOT NULL
            """, (payload['usuario_id'],))
            stats = cur.fetchone()
            
            # Tareas pendientes
            pendientes = total_tareas - stats['calificadas']
            
            cur.close()
            
            return jsonify({
                'exito': True,
                'estadisticas': {
                    'total_tareas': total_tareas,
                    'calificadas': stats['calificadas'],
                    'pendientes': pendientes,
                    'promedio': round(stats['promedio'], 2) if stats['promedio'] else 0
                }
            }), 200
            
        except Exception as e:
            print(f"Error en obtener_estadisticas_estudiante: {e}")
            return jsonify({'exito': False, 'mensaje': 'Error en el servidor'}), 500
    
    return calificaciones_bp
