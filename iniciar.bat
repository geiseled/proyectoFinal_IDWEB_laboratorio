@echo off
REM ============================================
REM Script de Inicio - Colegio Miguel Grau
REM ============================================

echo.
echo ================================================
echo   Sistema de Gestion Educativa
echo   Colegio Miguel Grau
echo ================================================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv" (
    echo [INFO] Creando entorno virtual...
    python -m venv venv
    echo [OK] Entorno virtual creado
    echo.
)

REM Activar entorno virtual
echo [INFO] Activando entorno virtual...
call venv\Scripts\activate
echo.

REM Instalar dependencias
echo [INFO] Instalando dependencias...
pip install -r requirements.txt --quiet
echo [OK] Dependencias instaladas
echo.

REM Iniciar servidor
echo ================================================
echo   Iniciando servidor en http://localhost:5000
echo   Presiona Ctrl+C para detener el servidor
echo ================================================
echo.

python app.py

pause
