# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- Configuración del Negocio ---
N_PRODUCTOS = 150
N_CLIENTES = 55
N_VENTAS = 300
FECHA_INICIO = datetime(2024, 1, 1)
FECHA_FIN = datetime(2024, 12, 31)

MARCAS = ['Nike', 'Adidas', 'Reebok', 'Under Armour', 'Salomon', 'Puma']
CATEGORIAS = ['Zapatillas', 'Camiseta', 'Pantalón', 'Sudadera', 'Accesorios', 'Calcetines']
TALLAS_ROPA = ['S', 'M', 'L', 'XL']
TALLAS_ZAPATILLAS = [str(i) for i in np.arange(38, 45.5, 0.5)]

# =================================================================
# 1. GENERAR DIM_PRODUCTO (150 Artículos)
# =================================================================
data_productos = []
for i in range(1, N_PRODUCTOS + 1):
    marca = np.random.choice(MARCAS)
    categoria = np.random.choice(CATEGORIAS)
    
    if categoria == 'Zapatillas':
        talla = np.random.choice(TALLAS_ZAPATILLAS)
        precio = round(np.random.uniform(70, 180), 2)
    elif categoria == 'Accesorios' or categoria == 'Calcetines':
        talla = 'Única'
        precio = round(np.random.uniform(10, 30), 2)
    else:
        talla = np.random.choice(TALLAS_ROPA)
        precio = round(np.random.uniform(30, 90), 2)
        
    costo = round(precio * np.random.uniform(0.35, 0.55), 2) # Costo 35%-55% del precio

    data_productos.append({
        'ID_Producto': i,
        'Nombre_Producto': f'{marca} {categoria} Modelo {i}',
        'Marca': marca,
        'Categoría': categoria,
        'Talla': talla,
        'Precio_Unitario': precio,
        'Costo_Unitario': costo
    })

df_productos = pd.DataFrame(data_productos)

# =================================================================
# 2. GENERAR DIM_CLIENTE (>50 Clientes)
# =================================================================
CIUDADES = ['Madrid', 'Barcelona', 'CDMX', 'Bogotá', 'Santiago', 'Buenos Aires', 'Lima']
PAISES = ['España', 'México', 'Colombia', 'Chile', 'Argentina', 'Perú']

data_clientes = []
for i in range(1, N_CLIENTES + 1):
    pais = np.random.choice(PAISES)
    fecha_registro = FECHA_INICIO - timedelta(days=np.random.randint(30, 365))
    
    data_clientes.append({
        'ID_Cliente': i,
        'Nombre': f'Cliente {i}',
        'Email': f'cliente{i}@tienda.com',
        'Ciudad': np.random.choice(CIUDADES),
        'País': pais,
        'Fecha_Registro': fecha_registro.strftime('%Y-%m-%d')
    })
    
df_clientes = pd.DataFrame(data_clientes)

# =================================================================
# 3. GENERAR FACT_VENTA (~300 Ventas en 2024)
# =================================================================
data_ventas = []
product_ids = df_productos['ID_Producto'].tolist()
customer_ids = df_clientes['ID_Cliente'].tolist()
date_range = [FECHA_INICIO + timedelta(days=i) for i in range((FECHA_FIN - FECHA_INICIO).days + 1)]

for i in range(1, N_VENTAS + 1):
    fecha_venta = np.random.choice(date_range)
    id_producto = np.random.choice(product_ids)
    id_cliente = np.random.choice(customer_ids)
    cantidad = np.random.choice([1, 1, 1, 2, 3]) # Más probabilidad de vender solo 1
    
    precio_unitario = df_productos[df_productos['ID_Producto'] == id_producto]['Precio_Unitario'].iloc[0]
    
    # Simular descuentos
    descuento = 0.0 if np.random.rand() > 0.8 else np.random.choice([0.05, 0.1, 0.15])
    
    precio_venta_total = round(precio_unitario * cantidad, 2)
    
    data_ventas.append({
        'ID_Venta': 10000 + i,
        'Fecha_Venta': fecha_venta.strftime('%Y-%m-%d'),
        'ID_Cliente': id_cliente,
        'ID_Producto': id_producto,
        'Cantidad': cantidad,
        'Precio_Venta_Total': precio_venta_total,
        'Descuento_Aplicado': descuento
    })

df_ventas = pd.DataFrame(data_ventas)

# =================================================================
# 4. GENERAR FACT_ENVIO (Relacionado con las Ventas)
# =================================================================
data_envios = []
for index, row in df_ventas.iterrows():
    id_venta = row['ID_Venta']
    fecha_venta = datetime.strptime(row['Fecha_Venta'], '%Y-%m-%d')
    
    fecha_envio = fecha_venta + timedelta(days=np.random.randint(1, 3))
    
    # 85% Finalizado, 15% En Proceso/Enviado
    if np.random.rand() < 0.85:
        estado = 'Finalizado'
        fecha_entrega_real = fecha_envio + timedelta(days=np.random.randint(3, 8))
        fecha_entrega_real = fecha_entrega_real.strftime('%Y-%m-%d')
    else:
        estado = np.random.choice(['En Proceso', 'Enviado'])
        fecha_entrega_real = None # Nulo si no ha terminado
    
    fecha_entrega_estimada = fecha_envio + timedelta(days=5)
    costo_envio = round(np.random.uniform(3, 10), 2)
    
    data_envios.append({
        'ID_Venta': id_venta,
        'Fecha_Envio': fecha_envio.strftime('%Y-%m-%d'),
        'Fecha_Entrega_Estimada': fecha_entrega_estimada.strftime('%Y-%m-%d'),
        'Fecha_Entrega_Real': fecha_entrega_real,
        'Estado_Envio': estado,
        'Costo_Envio': costo_envio
    })

df_envios = pd.DataFrame(data_envios)


# =================================================================
# 5. EXPORTAR A CSV
# =================================================================
df_productos.to_csv('dim_producto.csv', index=False)
df_clientes.to_csv('dim_cliente.csv', index=False)
df_ventas.to_csv('fact_venta.csv', index=False)
df_envios.to_csv('fact_envio.csv', index=False)

print("¡Archivos CSV generados con éxito!")