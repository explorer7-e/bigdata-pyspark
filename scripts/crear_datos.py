#!/usr/bin/env python3
import pandas as pd
import os

# Crear directorio de datos
os.makedirs("data", exist_ok=True)

# Datos de ventas
ventas_data = {
    'venta_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'producto_id': [101, 102, 101, 103, 104, 102, 101, 103, 104, 105],
    'cantidad': [2, 1, 3, 2, 1, 4, 2, 1, 3, 2],
    'precio_unitario': [10.5, 25.0, 10.5, 15.75, 30.0, 25.0, 10.5, 15.75, 30.0, 8.99],
    'fecha': ['2024-01-15', '2024-01-15', '2024-01-16', '2024-01-16', 
              '2024-01-17', '2024-01-17', '2024-01-18', '2024-01-18', 
              '2024-01-19', '2024-01-19'],
    'cliente_id': [1001, 1002, 1001, 1003, 1004, 1002, 1005, 1003, 1004, 1006]
}

# Datos de productos
productos_data = {
    'producto_id': [101, 102, 103, 104, 105],
    'nombre': ['Laptop', 'Mouse', 'Teclado', 'Monitor', 'USB'],
    'categoria': ['Electrónica', 'Accesorio', 'Accesorio', 'Electrónica', 'Accesorio'],
    'stock': [50, 200, 150, 75, 300]
}

# Crear DataFrames de pandas
df_ventas = pd.DataFrame(ventas_data)
df_productos = pd.DataFrame(productos_data)

# Guardar como CSV
df_ventas.to_csv('data/ventas.csv', index=False)
df_productos.to_csv('data/productos.csv', index=False)

print("✅ Datos creados exitosamente:")
print(f"📊 Ventas: {len(df_ventas)} registros")
print(f"📦 Productos: {len(df_productos)} registros")
