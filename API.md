# 📡 Documentación de la API

## URL Base
```
http://localhost:5000/api
```

## Autenticación

Todos los endpoints protegidos requieren un token JWT en el header:
```
Authorization: Bearer <token>
```

---

## 🔐 Endpoints de Autenticación

### 1. Registro de Profesor
```http
POST /api/registro/profesor
```

**Body (JSON):**
```json
{
  "id": "PROF001",
  "nombres": "Carlos",
  "apellidos": "Mendoza",
  "dni": "12345678",
  "correo": "carlos@gmail.com",
  "contrasena": "pass123",
  "especialidad": "Matemáticas"
}
```

**Respuesta Exitosa (201):**
```json
{
  "exito": true,
  "mensaje": "Registro exitoso. Ahora puedes iniciar sesión."
}
```

---

### 2. Registro de Estudiante
```http
POST /api/registro/estudiante
```

**Body (JSON):**
```json
{
  "id": "EST001",
  "nombres": "Ana",
  "apellidos": "García",
  "dni": "87654321",
  "correo": "ana@gmail.com",
  "contrasena": "pass123",
  "grado": "5to",
  "seccion": "A"
}
```

**Respuesta Exitosa (201):**
```json
{
  "exito": true,
  "mensaje": "Registro exitoso. Ahora puedes iniciar sesión."
}
```

---

### 3. Iniciar Sesión
```http
POST /api/login
```

**Body (JSON):**
```json
{
  "id": "PROF001",
  "contrasena": "pass123"
}
```

**Respuesta Exitosa (200):**
```json
{
  "exito": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "usuario": {
    "id": "PROF001",
    "nombres": "Carlos",
    "apellidos": "Mendoza",
    "correo": "carlos@gmail.com",
    "tipo": "profesor"
  },
  "mensaje": "Bienvenido, Carlos!"
}
```

---

## 📚 Endpoints de Tareas

### 4. Crear Tarea (Profesor)
```http
POST /api/tareas
Authorization: Bearer <token>
```

**Body (JSON):**
```json
{
  "titulo": "Resolver Ecuaciones",
  "descripcion": "Resolver ejercicios del 1 al 15",
  "curso": "Matemática",
  "fechaEntrega": "2025-01-30",
  "tipo": "tarea",
  "puntos": 20
}
```

**Respuesta Exitosa (201):**
```json
{
  "exito": true,
  "tarea_id": 1,
  "mensaje": "Tarea creada exitosamente"
}
```

---

### 5. Obtener Tareas del Profesor
```http
GET /api/tareas/profesor
Authorization: Bearer <token>
```

**Respuesta Exitosa (200):**
```json
{
  "exito": true,
  "tareas": [
    {
      "id": 1,
      "titulo": "Resolver Ecuaciones",
      "descripcion": "Resolver ejercicios del 1 al 15",
      "curso": "Matemática",
      "fecha_entrega": "2025-01-30",
      "puntos": 20,
      "total_entregas": 15,
      "calificadas": 10
    }
  ]
}
```

---

### 6. Obtener Tareas del Estudiante
```http
GET /api/tareas/estudiante
Authorization: Bearer <token>
```

**Respuesta Exitosa (200):**
```json
{
  "exito": true,
  "tareas": [
    {
      "id": 1,
      "titulo": "Resolver Ecuaciones",
      "curso": "Matemática",
      "fecha_entrega": "2025-01-30",
      "profesor_nombres": "Carlos",
      "profesor_apellidos": "Mendoza",
      "nota": 18,
      "comentario": "Excelente trabajo",
      "estado_entrega": "calificada",
      "dias_restantes": 5
    }
  ]
}
```

---

### 7. Eliminar Tarea (Profesor)
```http
DELETE /api/tareas/<tarea_id>
Authorization: Bearer <token>
```

**Respuesta Exitosa (200):**
```json
{
  "exito": true,
  "mensaje": "Tarea eliminada"
}
```

---

## 📊 Endpoints de Calificaciones

### 8. Asignar Calificación (Profesor)
```http
POST /api/calificaciones
Authorization: Bearer <token>
```

**Body (JSON):**
```json
{
  "tarea_id": 1,
  "estudiante_id": "EST001",
  "nota": 18,
  "comentario": "Excelente trabajo"
}
```

**Respuesta Exitosa (200):**
```json
{
  "exito": true,
  "mensaje": "Calificación asignada exitosamente"
}
```

---

### 9. Obtener Entregas de una Tarea (Profesor)
```http
GET /api/calificaciones/tarea/<tarea_id>/entregas
Authorization: Bearer <token>
```

**Respuesta Exitosa (200):**
```json
{
  "exito": true,
  "entregas": [
    {
      "id": "EST001",
      "nombres": "Ana",
      "apellidos": "García",
      "nota": 18,
      "comentario": "Excelente trabajo",
      "fecha_calificacion": "2025-01-15T10:30:00",
      "estado": "calificada"
    }
  ]
}
```

---

### 10. Obtener Estadísticas del Estudiante
```http
GET /api/calificaciones/estudiante/estadisticas
Authorization: Bearer <token>
```

**Respuesta Exitosa (200):**
```json
{
  "exito": true,
  "estadisticas": {
    "total_tareas": 20,
    "calificadas": 15,
    "pendientes": 5,
    "promedio": 16.5
  }
}
```

---

## 🏥 Endpoints de Sistema

### 11. Health Check
```http
GET /api/health
```

**Respuesta Exitosa (200):**
```json
{
  "status": "OK",
  "mensaje": "Servidor funcionando correctamente",
  "database": "OK",
  "timestamp": "2025-01-15T10:30:00"
}
```

---

## ❌ Códigos de Error

| Código | Descripción |
|--------|-------------|
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - Token inválido o faltante |
| 403 | Forbidden - Sin permisos |
| 404 | Not Found - Recurso no encontrado |
| 500 | Internal Server Error - Error del servidor |

**Formato de Error:**
```json
{
  "exito": false,
  "mensaje": "Descripción del error"
}
```

---

## 🔒 Validaciones

### DNI
- Exactamente 8 dígitos numéricos
- Ejemplo: `12345678`

### Correo
- Debe ser una cuenta de Gmail
- Formato: `usuario@gmail.com`

### Contraseña
- Mínimo 6 caracteres
- Debe contener al menos un número

### ID de Profesor
- Formato: `PROF###`
- Ejemplo: `PROF001`, `PROF123`

### ID de Estudiante
- Formato: `EST###`
- Ejemplo: `EST001`, `EST456`

### Notas
- Rango: 0 - 20
- Tipo: Número decimal

---

## 📝 Notas Adicionales

- Todos los timestamps están en formato ISO 8601
- Las fechas de entrega deben ser en formato `YYYY-MM-DD`
- Los tokens JWT expiran después de 24 horas
- El servidor usa el puerto 5000 por defecto
