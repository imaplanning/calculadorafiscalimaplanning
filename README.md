import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------

# CONFIGURACIÓN DE PÁGINA Y LOGO

# -------------------------------

st.set\_page\_config(page\_title="Calculadora Fiscal Imaplanning", page\_icon="💼", layout="wide")
st.image("logo.png", width=180)  # Logo local de Imaplanning

st.title("💼 Calculadora de Beneficios Fiscales")
st.subheader("Artículo 151 LISR + Proyección de Retiro")

# -------------------------------

# ENTRADAS DEL USUARIO

# -------------------------------

ingreso\_mensual = st.number\_input("🔹 Ingreso mensual (MXN)", min\_value=10000, step=1000, value=40000)
edad\_actual = st.slider("🔹 Edad actual", 18, 60, 35)
tasa\_rendimiento = st.slider("🔹 Tasa anual esperada de inversión (%)", 8, 15, 10) / 100
inflacion = st.slider("🔹 Inflación anual (%)", 2, 7, 4) / 100

# -------------------------------

# CÁLCULO ISR SIMPLIFICADO

# -------------------------------

ingreso\_anual = ingreso\_mensual \* 12
tope\_deducciones = min(ingreso\_anual \* 0.15, 5 \* 172872)  # Tope 5 UMA aprox.

def calcular\_isr(anual):
if anual <= 7735:
return anual \* 0.0192
elif anual <= 65651:
return 148.51 + (anual - 7735) \* 0.064
elif anual <= 115375:
return 3856.6 + (anual - 65651) \* 0.1088
elif anual <= 134119:
return 9265.2 + (anual - 115375) \* 0.16
elif anual <= 160577:
return 12508.6 + (anual - 134119) \* 0.1792
elif anual <= 323862:
return 17688.2 + (anual - 160577) \* 0.2136
elif anual <= 510451:
return 51458.2 + (anual - 323862) \* 0.2352
else:
return 94356.8 + (anual - 510451) \* 0.30

isr\_sin\_deduccion = calcular\_isr(ingreso\_anual)
isr\_con\_deduccion = calcular\_isr(ingreso\_anual - tope\_deducciones)
devolucion = isr\_sin\_deduccion - isr\_con\_deduccion

# -------------------------------

# PROYECCIÓN DE RETIRO HASTA 65 AÑOS

# -------------------------------

años\_restantes = 65 - edad\_actual
aportacion\_inicial = ingreso\_anual \* 0.10

capital = 0
aportaciones = \[]
años = \[]
for año in range(1, años\_restantes + 1):
aportacion = aportacion\_inicial \* ((1 + inflacion) \*\* (año - 1))
capital = (capital + aportacion + devolucion) \* (1 + tasa\_rendimiento)
aportaciones.append(capital)
años.append(edad\_actual + año)

# -------------------------------

# RESULTADOS EN STREAMLIT

# -------------------------------

col1, col2 = st.columns(2)
with col1:
st.metric("ISR sin deducción", f"\${isr\_sin\_deduccion:,.0f}")
st.metric("ISR con deducción", f"\${isr\_con\_deduccion:,.0f}")
with col2:
st.metric("Posible devolución anual", f"\${devolucion:,.0f}")
st.metric("Capital estimado a los 65", f"\${capital:,.0f}")

# -------------------------------

# GRÁFICO DE PROYECCIÓN

# -------------------------------

fig, ax = plt.subplots()
ax.plot(años, aportaciones, label="Proyección inversión + devolución fiscal")
ax.set\_xlabel("Edad")
ax.set\_ylabel("Capital acumulado (MXN)")
ax.legend()
st.pyplot(fig)

st.info("⚡ Esta es una simulación ilustrativa; los resultados pueden variar según condiciones fiscales y de mercado.")
