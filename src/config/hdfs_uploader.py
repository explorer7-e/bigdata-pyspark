#!/usr/bin/env python3
"""
hdfs_uploader.py

Módulo para subir archivos a HDFS de forma interactiva y automatizada.
"""

import os
import subprocess
from datetime import datetime

def subir_a_hdfs(local_path=None, hdfs_dir="/data/pyspark"):
    """
    Sube un archivo local a HDFS.

    Args:
        local_path (str, optional): Ruta del archivo local. Si no se pasa, se pide al usuario.
        hdfs_dir (str): Carpeta destino en HDFS.

    Returns:
        str: Ruta completa del archivo en HDFS.
    """

    # 📂 Si no se proporciona la ruta, pedir al usuario
    if not local_path:
        local_path = input("📂 Ingresa la ruta completa del archivo a subir: ").strip()

    # Verificar que el archivo exista
    if not os.path.isfile(local_path):
        raise FileNotFoundError(f"❌ El archivo '{local_path}' no existe.")

    # Extraer nombre base
    file_name = os.path.basename(local_path)

    # Generar nombre único con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_name = f"{timestamp}_{file_name}"

    # Ruta final en HDFS
    hdfs_path = f"{hdfs_dir}/{new_name}"

    print(f"🚀 Subiendo archivo como: {new_name}")

    # Crear carpeta en HDFS si no existe
    try:
        subprocess.run(["hdfs", "dfs", "-mkdir", "-p", hdfs_dir], check=True, timeout=30)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creando carpeta en HDFS: {e}")
        raise

    # Subir archivo a HDFS
    try:
        subprocess.run(["hdfs", "dfs", "-put", "-f", local_path, hdfs_path], check=True, timeout=30)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error subiendo archivo a HDFS: {e}")
        raise

    # Listar contenido de la carpeta en HDFS
    subprocess.run(["hdfs", "dfs", "-ls", hdfs_dir], timeout=30)

    print(f"✅ Archivo cargado correctamente en HDFS: {hdfs_path}")

    return hdfs_path

if __name__ == "__main__":
    # Permite ejecutar directamente el módulo
    try:
        subir_a_hdfs()
    except Exception as e:
        print(e)
