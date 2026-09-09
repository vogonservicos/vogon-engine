import streamlit as st
import numpy as np

# Configuração da página da Vogon
st.set_page_config(page_title="Vogon Group - Engenharia", page_icon="⚙️", layout="wide")

st.title("⚙️ Vogon Group — Calculadora Técnica")
st.caption("Dimensionamento de Doctoring Systems & Chuveiros")

st.header("1. Dimensionamento Estrutural do Porta-Lâminas")

# Entrada de dados simples pelo usuário
comprimento_mm = st.number_input("Comprimento Nominal da Viga/Rolo (mm)", value=4500, step=100)
pressao_linear = st.number_input("Pressão Linear Desejada (N/m)", value=350, step=10)

material = st.selectbox(
    "Material da Estrutura",
    ["Aço Carbono (E = 210 GPa)", "Aço Inox 316L (E = 193 GPa)", "Bronze / Alumínio (E = 110 GPa)"]
)

inercia = st.number_input("Momento de Inércia do Perfil (cm⁴)", value=1250, step=50)

# Mapeamento do módulo de elasticidade
e_map = {"Aço Carbono (E = 210 GPa)": 210, "Aço Inox 316L (E = 193 GPa)": 193, "Bronze / Alumínio (E = 110 GPa)": 110}
E_GPa = e_map[material]

# Cálculos em unidades SI
L = comprimento_mm / 1000.0
w = pressao_linear
E = E_GPa * 1e9
I = inercia * 1e-8

# Deflexão Máxima (mm)
deflexao_mm = ((5 * w * (L**4)) / (384 * E * I)) * 1000.0
limite_admissivel_mm = comprimento_mm / 1500.0

col1, col2 = st.columns(2)
with col1:
    st.metric("Deflexão Estimada", f"{deflexao_mm:.3f} mm")
with col2:
    st.metric("Limite Tolerado (L/1500)", f"{limite_admissivel_mm:.3f} mm")

if deflexao_mm <= limite_admissivel_mm:
    st.success("✅ **APROVADO:** A deflexão está dentro das tolerâncias do fabricante. Raspagem uniforme assegurada!")
else:
    st.error("⚠️ **ALERTA:** Deflexão excessiva! Recomendado reforçar o perfil da viga para evitar desgaste irregular do rolo.")

st.divider()

st.header("2. Estimativa de Consumo de Água (Chuveiros de Limpeza)")
bicos = st.number_input("Quantidade de Bicos do Chuveiro", value=30, step=1)
pressao_bar = st.number_input("Pressão de Operação (bar)", value=15, step=1)

# Cálculo de vazão aproximada por bico (L/min) em função da pressão
vazao_total_lmin = bicos * (1.2 * np.sqrt(pressao_bar))
vazao_m3h = (vazao_total_lmin * 60) / 1000.0

st.metric("Vazão Total de Água Requerida", f"{vazao_total_lmin:.1f} L/min", f"{vazao_m3h:.2f} m³/h")

st.info("💡 **Dica Vogon:** Com o nosso sistema de bicos autolimpantes com oscilação programada, é possível reduzir esse consumo em até 20% mantendo a eficiência de lavagem da tela.")
