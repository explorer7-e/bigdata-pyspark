from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import DecimalType

class TransformacionesVentas:
    def __init__(self, spark):
        self.spark = spark
    
    def cargar_datos(self):
        """Carga los datos desde archivos CSV"""
        print("📂 Cargando datos...")
        
        ventas_df = self.spark.read.csv(
            "file:///home/hadoop/bigdata-spark/data/ventas.csv",
            header=True,
            inferSchema=True
        )
        
        productos_df = self.spark.read.csv(
            "file:///home/hadoop/bigdata-spark/data/productos.csv",
            header=True,
            inferSchema=True
        )
        
        return ventas_df, productos_df
    
    def calcular_metricas(self, ventas_df, productos_df):
        """Calcula métricas de ventas"""
        
        # Calcular venta total por transacción
        ventas_df = ventas_df.withColumn(
            "venta_total",
            F.col("cantidad") * F.col("precio_unitario")
        )
        
        # Unir con productos
        ventas_completas_df = ventas_df.join(
            productos_df,
            "producto_id",
            "inner"
        )
        
        # Métricas agregadas
        metricas_df = ventas_completas_df.groupBy(
            "categoria", "nombre"
        ).agg(
            F.sum("cantidad").alias("total_vendido"),
            F.sum("venta_total").alias("ingresos_totales"),
            F.avg("precio_unitario").alias("precio_promedio"),
            F.count("*").alias("transacciones")
        ).orderBy(F.desc("ingresos_totales"))
        
        return ventas_completas_df, metricas_df
    
    def analisis_temporal(self, ventas_df):
        """Análisis de ventas por fecha"""
        
        ventas_df = ventas_df.withColumn("fecha", F.to_date("fecha"))
        
        analisis_temporal_df = ventas_df.groupBy(
            "fecha"
        ).agg(
            F.sum("cantidad").alias("total_unidades"),
            F.sum(F.col("cantidad") * F.col("precio_unitario")).alias("venta_diaria"),
            F.countDistinct("cliente_id").alias("clientes_unicos"),
            F.avg("precio_unitario").alias("precio_promedio_diario")
        ).orderBy("fecha")
        
        return analisis_temporal_df
    
    def top_clientes(self, ventas_df, top_n=3):
        """Identifica los mejores clientes"""
        
        clientes_df = ventas_df.groupBy(
            "cliente_id"
        ).agg(
            F.sum("cantidad").alias("total_compras"),
            F.sum(F.col("cantidad") * F.col("precio_unitario")).alias("gasto_total")
        ).orderBy(F.desc("gasto_total")).limit(top_n)
        
        return clientes_df
