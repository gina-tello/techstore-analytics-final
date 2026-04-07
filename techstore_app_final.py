import streamlit as st
import pandas as pd
import numpy as np

st.caption("Proyecto final de Machine Learning y Analítica - TechStore")

st.set_page_config(page_title="TechStore Analytics", layout="wide")

st.title("📊 TechStore Analytics Dashboard")
st.markdown("Sistema final de analítica, predicción y segmentación para TechStore")

@st.cache_data
def cargar_datos():
    ventas = pd.read_csv("ventas_historicas.csv")
    clientes = pd.read_csv("clientes_segmentados.csv")
    return ventas, clientes

ventas, clientes = cargar_datos()

clientes_totales = len(clientes)
ventas_promedio = ventas["ventas"].mean()
elasticidad = 0.37876067728294854

col1, col2, col3 = st.columns(3)
col1.metric("Clientes totales", f"{clientes_totales:,}")
col2.metric("Ventas promedio", f"{ventas_promedio:,.2f}")
col3.metric("Elasticidad", f"{elasticidad:.2f}")

st.divider()

st.subheader("Ventas históricas")
if "fecha" in ventas.columns:
    ventas["fecha"] = pd.to_datetime(ventas["fecha"], errors="coerce")
    ventas_ordenadas = ventas.sort_values("fecha")
    st.line_chart(ventas_ordenadas.set_index("fecha")["ventas"])
else:
    st.line_chart(ventas["ventas"])

st.divider()

st.subheader("Distribución de ventas")
st.bar_chart(ventas["ventas"])

st.divider()

st.subheader("Segmentación de clientes")
columnas_numericas = clientes.select_dtypes(include=np.number).columns.tolist()

if "segmento" in clientes.columns:
    st.write("Clientes por segmento")
    conteo_segmentos = clientes["segmento"].value_counts()
    st.bar_chart(conteo_segmentos)
elif len(columnas_numericas) >= 2:
    eje_x = columnas_numericas[0]
    eje_y = columnas_numericas[1]
    st.write(f"Visualización de {eje_x} vs {eje_y}")
    st.scatter_chart(clientes[[eje_x, eje_y]])
else:
    st.write("No se encontraron columnas suficientes para mostrar la segmentación.")

st.divider()

st.subheader("Hallazgos clave")
st.markdown("""
- Se analizaron **2,000 clientes** dentro del sistema.
- El promedio de ventas es de **77,210.78**.
- La elasticidad estimada es de **0.38**, lo que sugiere una **baja sensibilidad al precio**.
- Esto abre oportunidades para **optimizar precios y mejorar márgenes**.
""")
