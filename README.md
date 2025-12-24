# 🏫 Sistema de Gestión Educativa - Colegio Miguel Grau

## 📋 Descripción del Proyecto

Sistema web completo para la gestión de tareas y calificaciones educativas, desarrollado como proyecto final del curso de Desarrollo Web. Permite a profesores crear y gestionar tareas, calificar estudiantes, y a los estudiantes visualizar sus asignaciones y calificaciones en tiempo real.

## Equipo de Desarrollo

**Nombre del Equipo:** [Colegio Miguel Grau - Sistema de Gestión Educativa]

**Líder del Equipo:** [Condori Choccata Anthony Moises]

### Integrantes:
1. **Condori Choccata Anthony Moises** - []
2. **Chipayo Paco Santos Christian** - []  
3. **Pacheco Medina Geisel Reymar** - []

## Tecnologías Utilizadas

### Frontend
- **HTML5** - Estructura y contenido
- **CSS3** - Estilos y diseño responsivo
- **JavaScript (ES6+)** - Interactividad y logica del cliente

### Backend
- **Python 3.12+** - Lenguaje de programación
- **Flask** - Framework web
- **Flask-CORS** - Manejo de CORS
- **Flask-MySQLdb** - Conexión con MySQL
- **PyJWT** - Autenticación con tokens

### Base de Datos
- **MySQL 8.0+** - Sistema de gestion de base de datos

### Herramientas
- **Git/GitHub** - Control de versiones
- **Docker** - Contenerizacion

## Estructura del Proyecto

```t
proyecto_colegio/Piloto/
├── backend/                    # Módulos del backend
│   ├── __init__.py
│   ├── config.py              # Configuración de la app
│   ├── utils.py               # Utilidades y validaciones
│   ├── auth_routes.py         # Rutas de autenticación
│   ├── tareas_routes.py       # Rutas de tareas
│   └── calificaciones_routes.py  # Rutas de calificaciones
├── images/                     # Imágenes del sitio
│   ├── landingimage.png
│   ├── miguelgrau.png
│   └── ...
├── javascript/                 # Scripts del frontend
│   ├── control_sistema.js     # Sistema principal
│   ├── registro_profesor.js
│   ├── registro_estudiante.js
│   ├── interfaz_profesor.js
│   └── interfaz_estudiante.js
├── pages/                      # Páginas HTML
│   ├── header.html            # Header reutilizable
│   ├── footer.html            # Footer reutilizable
│   ├── acercade.html          # Página de información
│   ├── registro_profesor.html
│   ├── registro_estudiante.html
│   ├── interfaz_profesor.html
│   └── interfaz_estudiante.html
├── styles/                     # Hojas de estilo
│   ├── style.css              # Estilos globales
│   ├── header.css
│   ├── footer.css
│   ├── index.css
│   └── ...
├── app.py                      # Aplicación Flask principal
├── BD.sql                      # Script de base de datos
├── configuracion.env           # Variables de entorno
├── Dockerfile                  # Configuración Docker
├── requirements.txt            # Dependencias Python
├── index.html                  # Página principal
├── login.html                  # Página de login
└── README.md                   # Este archivo
```

## Funcionalidades Implementadas

### 1. Sistema de Autenticación
- Registro de profesores con validación
- Registro de estudiantes con validación
- Login con JWT tokens
- Validación de DNI (8 dígitos)
- Validación de correos Gmail
- Contraseñas seguras (mínimo 6 caracteres + número)

### 2. Panel de Profesores
- Crear tareas con detalles completos
- Ver listado de todas sus tareas
- Asignar calificaciones a estudiantes
- Eliminar tareas creadas
- Ver estadísticas de entregas

### 3. Panel de Estudiantes
- Ver todas las tareas asignadas
- Consultar calificaciones
- Ver estadísticas personales
- Filtrar tareas por estado

### 4. Frontend Interactivo
- Diseño responsivo (mobile-first)
- Validación de formularios en tiempo real
- Animaciones y transiciones suaves
- Indicadores de fortaleza de contraseña
- Alertas y notificaciones visuales
- Navegación dinámica entre páginas

### 5. Backend Modular
- Arquitectura en capas
- Rutas organizadas por blueprints
- Validaciones robustas
- Manejo de errores centralizado
- Operaciones CRUD completas

## Instalación y Configuración

### Requisitos Previos
```bash
# Verificar versiones instaladas
python --version  # 3.12 o superior
mysql --version   # 8.0 o superior
git --version
```

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/geiseled/proyectoFinal_IDWEB_laboratorio.git
cd proyecto_colegio/Piloto
```

### Paso 2: Configurar Base de Datos
```bash
# Iniciar MySQL
mysql -u root -p

# Crear la base de datos
mysql> source BD.sql
# o
mysql> CREATE DATABASE colegio_miguel_grau;
mysql> USE colegio_miguel_grau;
mysql> source BD.sql
```

### Paso 3: Configurar Variables de Entorno
Editar `backend/config.py`:
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'tu_contraseña_mysql'
MYSQL_DB = 'colegio_miguel_grau'
```

### Paso 4: Instalar Dependencias
```bash
# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 5: Ejecutar la Aplicación
```bash
# Iniciar el servidor backend
python app.py

# El servidor iniciará en http://localhost:5000
```

### Paso 6: Abrir el Frontend
```bash
# Abrir index.html en el navegador
# O usar un servidor local:
python -m http.server 8000
# Luego abrir: http://localhost:8000
```

## Ejecutar con Docker

### Construir la Imagen
```bash
docker build -t colegio-miguel-grau .
```

### Ejecutar el Contenedor
```bash
docker run -p 5000:5000 colegio-miguel-grau
```

La aplicación estará disponible en `http://localhost:5000`

## Testing

### Datos de Prueba

#### Profesores:
```
ID: PROF001
Contraseña: 123456
```

#### Estudiantes:
```
ID: EST001
Contraseña: 123456
```

### Endpoints de la API

#### Autenticación
```
POST /api/registro/profesor
POST /api/registro/estudiante
POST /api/login
```

#### Tareas
```
POST   /api/tareas              - Crear tarea
GET    /api/tareas/profesor     - Obtener tareas del profesor
GET    /api/tareas/estudiante   - Obtener tareas del estudiante
DELETE /api/tareas/:id          - Eliminar tarea
```

#### Calificaciones
```
POST /api/calificaciones                        - Asignar calificación
GET  /api/calificaciones/tarea/:id/entregas    - Ver entregas de una tarea
GET  /api/calificaciones/estudiante/estadisticas - Estadísticas del estudiante
```

## 📸 Capturas de Pantalla

[Aquí agregar capturas de las principales pantallas]

## Manual de Usuario

### Para Profesores:
1. Registrarse con ID formato `PROF###`
2. Iniciar sesión
3. Crear tareas desde el panel
4. Calificar estudiantes
5. Ver estadísticas

### Para Estudiantes:
1. Registrarse con ID formato `EST###`
2. Iniciar sesión
3. Ver tareas asignadas
4. Consultar calificaciones
5. Ver progreso académico

## Trabajo Futuro

- [ ] Sistema de notificaciones en tiempo real
- [ ] Chat entre profesores y estudiantes
- [ ] Carga de archivos adjuntos
- [ ] Exportación de reportes en PDF
- [ ] Dashboard con gráficos estadísticos
- [ ] App móvil nativa
- [ ] Sistema de asistencia
- [ ] Calendario académico integrado
- [ ] Mensajería interna

## Conclusiones

Este proyecto demuestra la aplicación práctica de tecnologías web modernas para resolver necesidades reales del sector educativo. Se logró desarrollar un sistema completo, funcional y escalable que integra:

- Frontend responsivo y dinámico
- Backend robusto con arquitectura modular
- Base de datos relacional bien diseñada
- Autenticación y seguridad
- Operaciones CRUD completas

El trabajo en equipo y la metodología ágil fueron fundamentales para completar exitosamente este proyecto.

## Bibliografía

- Flask Documentation: https://flask.palletsprojects.com/
- MySQL Documentation: https://dev.mysql.com/doc/
- MDN Web Docs: https://developer.mozilla.org/
- Python JWT: https://pyjwt.readthedocs.io/
- Docker Documentation: https://docs.docker.com/

## Licencia

Este proyecto fue desarrollado con fines educativos como parte del curso de Desarrollo Web.

## Contacto

Para consultas o sugerencias sobre el proyecto:

- [Pacheco Medina Geisel Reymar]: [gpachecome@unsa.edu.pe]


---

*Colegio Miguel Grau - Sistema de Gestión Educativa*
