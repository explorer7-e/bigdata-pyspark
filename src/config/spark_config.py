import os
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from dotenv import load_dotenv

load_dotenv()

def crear_spark_session(app_name="AnalisisVentas", master="local[*]"):
    """Crea y configura una sesión de Spark"""

    # Si ya existe una sesión activa, devolverla
    active = SparkSession.getActiveSession()
    if active:
        print("⚠ Reutilizando SparkSession existente")
        return active
    else:
        conf = SparkConf() \
            .setAppName(app_name) \
            .setMaster(master) \
            .set("spark.sql.warehouse.dir", "/tmp/spark-warehouse") \
            .set("javax.jdo.option.ConnectionURL", "jdbc:postgresql://localhost:5432/hive_metastore") \
            .set("javax.jdo.option.ConnectionDriverName", "org.postgresql.Driver") \
            .set("javax.jdo.option.ConnectionUserName", "username") \
            .set("javax.jdo.option.ConnectionPassword", "password") \
            .set("datanucleus.autoCreateSchema", "false")  # ya inicializaste el schema

    # Configurar Hive si está disponible
    try:
        spark = SparkSession.builder \
            .config(conf=conf) \
            .enableHiveSupport() \
            .getOrCreate()
        print("✅ Spark con soporte Hive inicializado")
    except Exception as e:
        print("⚠ No se pudo habilitar Hive:", e)
        spark = SparkSession.builder \
            .config(conf=conf) \
            .getOrCreate()
        print("✅ Spark sin Hive inicializado")

    # Configuraciones adicionales
    spark.sparkContext.setLogLevel("WARN")
    
    print(f"🔧 Spark version: {spark.version}")
    print(f"🔧 Hadoop version: {spark.sparkContext._jvm.org.apache.hadoop.util.VersionInfo.getVersion()}")
    
    return spark
    
def detener_spark_session(spark):
    """Detiene la sesión de Spark"""
    spark.stop()
    print("🔴 Sesión de Spark detenida")
