import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# CONFIGURACIÓN
# -------------------------------
st.set_page_config(page_title="Calculadora Fiscal Imaplanning", page_icon="💼", layout="wide")
st.image("https://i.ibb.co/4MPjHtx/imaplanning-logo.png", width=180)  # Logo Imaplanning

st.title("💼 Calculadora de Beneficios Fiscales")
st.subheader("Artículo 151 LISR + Proyección de Retiro")

# -------------------------------
# ENTRADAS DEL USUARIO
# -------------------------------
ingreso_mensual = st.number_input("🔹 Ingreso mensual (MXN)", min_value=10000, step=1000, value=40000)
edad_actual = st.slider("🔹 Edad actual", 18, 60, 35)
tasa_rendimiento = st.slider("🔹 Tasa anual esperada de inversión (%)", 8, 15, 10) / 100
inflacion = st.slider("🔹 Inflación anual (%)", 2, 7, 4) / 100

# -------------------------------
# PARÁMETROS
# -------------------------------
ingreso_anual = ingreso_mensual * 12
tope_deducciones = min(ingreso_anual * 0.15, 5 * 172_872)  # 5 UMAs anual aprox

# ISR simplificado (tabla 2025 ajustada)
def calcular_isr(anual):
    if anual <= 7735:
        return anual * 0.0192
    elif anual <= 65651:
        return 148.51 + (anual - 7735) * 0.064
    elif anual <= 115375:
        return 3856.6 + (anual - 65651) * 0.1088
    elif anual <= 134119:
        return 9265.2 + (anual - 115375) * 0.16
    elif anual <= 160577:
        return 12508.6 + (anual - 134119) * 0.1792
    elif anual <= 323862:
        return 17688.2 + (anual - 160577) * 0.2136
    elif anual <= 510451:
        return 51458.2 + (anual - 323862) * 0.2352
    else:
        return 94356.8 + (anual - 510451) * 0.30

# -------------------------------
# CÁLCULO ISR CON / SIN DEDUCCIONES
# -------------------------------
isr_sin_deduccion = calcular_isr(ingreso_anual)
isr_con_deduccion = calcular_isr(ingreso_anual - tope_deducciones)
devolucion = isr_sin_deduccion - isr_con_deduccion

# -------------------------------
# PROYECCIÓN A RETIRO (65 años)
# -------------------------------
años_restantes = 65 - edad_actual
aportacion_inicial = ingreso_anual * 0.10

capital = 0
aportaciones = []
años = []
for año in range(1, años_restantes + 1):
    aportacion = aportacion_inicial * ((1 + inflacion) ** (año - 1))
    capital = (capital + aportacion + devolucion) * (1 + tasa_rendimiento)
    aportaciones.append(capital)
    años.append(edad_actual + año)

# -------------------------------
# RESULTADOS
# -------------------------------
col1, col2 = st.columns(2)
with col1:
    st.metric("ISR sin deducción", f"${isr_sin_deduccion:,.0f}")
    st.metric("ISR con deducción", f"${isr_con_deduccion:,.0f}")
with col2:
    st.metric("Posible devolución anual", f"${devolucion:,.0f}")
    st.metric("Capital estimado a los 65", f"${capital:,.0f}")

# -------------------------------
# GRAFICAR PROYECCIÓN
# -------------------------------
fig, ax = plt.subplots()
ax.plot(años, aportaciones, label="Proyección con inversión + devolución fiscal")
ax.set_xlabel("Edad")
ax.set_ylabel("Capital acumulado (MXN)")
ax.legend()
st.pyplot(fig)

st.info("⚡ Este cálculo es una simulación con fines ilustrativos y puede variar según las condiciones fiscales y de mercado.")
