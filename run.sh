#!/bin/bash
# Script para ejecutar el proyecto

echo "🔧 Preparando entorno..."

#sudo su - hadoop

#start-dfs.sh
#start-yarn.sh
#hive --service metastore &
#sleep 10
#hive --service hiveserver2 &

# Actualiza sistema e Instala soporte de entornos virtuales
sudo apt update && sudo apt upgrade -y
sudo apt install python3.12-venv python3-full

# Eliminar el venv corrupto
sudo rm -rf venv

# Crear entorno virtual
python3 -m venv venv 2>/dev/null || echo "Virtualenv no disponible, continuando..."

# Activa el entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear datos de ejemplo
echo "📊 Creando datos de ejemplo..."
python3 scripts/crear_datos.py

# Ejecutar análisis
echo "🚀 Ejecutando análisis..."
python3 main.py

echo "✅ Análisis completado!"
echo "📁 Resultados en: resultados/"
