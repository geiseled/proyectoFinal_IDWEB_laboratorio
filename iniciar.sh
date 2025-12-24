#!/bin/bash
# ============================================
# Script de Inicio - Colegio Miguel Grau
# ============================================

echo ""
echo "================================================"
echo "  Sistema de Gestión Educativa"
echo "  Colegio Miguel Grau"
echo "================================================"
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "[INFO] Creando entorno virtual..."
    python3 -m venv venv
    echo "[OK] Entorno virtual creado"
    echo ""
fi

# Activar entorno virtual
echo "[INFO] Activando entorno virtual..."
source venv/bin/activate
echo ""

# Instalar dependencias
echo "[INFO] Instalando dependencias..."
pip install -r requirements.txt --quiet
echo "[OK] Dependencias instaladas"
echo ""

# Iniciar servidor
echo "================================================"
echo "  Iniciando servidor en http://localhost:5000"
echo "  Presiona Ctrl+C para detener el servidor"
echo "================================================"
echo ""

python app.py
