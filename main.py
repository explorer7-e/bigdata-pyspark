#!/usr/bin/env python3
"""
Script principal de análisis de ventas con PySpark
"""

import sys
import os

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__), './src'))

from config.spark_config import crear_spark_session, detener_spark_session
from etl.transformaciones import TransformacionesVentas

def main():
    """Función principal"""
    
    print("🚀 Iniciando análisis de ventas con PySpark")
    
    # Crear sesión de Spark
    spark = crear_spark_session("AnalisisVentas-Produccion")
    
    try:

        # Crear carpeta de resultados
        os.makedirs("resultados", exist_ok=True)

        # Inicializar transformaciones ETL
        transformaciones = TransformacionesVentas(spark)
        
        # Cargar datos
        ventas_df, productos_df = transformaciones.cargar_datos()
        
        print(f"\n📊 Datos cargados:")
        print(f"   - Ventas: {ventas_df.count()} registros")
        print(f"   - Productos: {productos_df.count()} registros")
        
        # Calcular métricas
        ventas_completas_df, metricas_df = transformaciones.calcular_metricas(
            ventas_df, productos_df
        )
        
        # Mostrar resultados
        print("\n🏆 Top productos por ingresos:")
        metricas_df.show(truncate=False)
        
        # Análisis temporal
        analisis_temporal_df = transformaciones.analisis_temporal(ventas_df)
        
        print("\n📅 Resumen diario:")
        analisis_temporal_df.show()
        
        # Top clientes
        top_clientes_df = transformaciones.top_clientes(ventas_df, top_n=3)
        
        print("\n👑 Top 3 clientes:")
        top_clientes_df.show()
        
        # Guardar resultados
        print("\n💾 Guardando resultados...")
        os.makedirs("resultados", exist_ok=True)

        base_path = "file:///home/hadoop/bigdata-spark/resultados"

        metricas_df.write.mode("overwrite").parquet(
            f"{base_path}/metricas_ventas.parquet"
        )

        ventas_completas_df.write.mode("overwrite").parquet(
            f"{base_path}/ventas_completas.parquet"
        )
        
        print("✅ Resultados guardados en carpeta 'resultados/'")
        
    except Exception as e:
        print(f"❌ Error durante la ejecucion: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Detener sesión de Spark
        detener_spark_session(spark)
        print("🔴 Sesión de Spark detenida correctamente")

if __name__ == "__main__":
    main()