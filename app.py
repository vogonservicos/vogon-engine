import streamlit as st
import pandas as pd

# Configuração da página Vogon no iOS/Navegador
st.set_page_config(
    page_title="Vogon Group - Calculadora de Chuveiros",
    page_icon="💧",
    layout="wide"
)

# Estilização visual com a marca Vogon
st.markdown("""
    <style>
    .main-title { font-size: 24px; font-weight: bold; color: #0E2F56; }
    .stButton>button { background-color: #0E2F56; color: white; border-radius: 6px; }
    </style>
""", unsafe_allow_html=True)

st.title("💧 Vogon Group — Engine de Vazão de Chuveiros")
st.caption("Cálculo Técnico de Consumo de Água baseado em Tabelas de Engenharia")

# MATRIZ DE DADOS EXTRAÍDA DA TABELA TÉCNICA (Modelo -> Pressão kg/cm² -> L/min)
# Dados extraídos diretamente da tabela técnica de vazão da Vogon / Concorrentes
dados_vazao = {
    "Modelo": [
        "FL-4/1", "FL-4/2", "FL-4/3", "FL-4/4", "FL-4/5", "FL-4/6", "FL-4/7", "FL-4/8", 
        "FL-4/9", "FL-4/10", "FL-4/11", "FL-4/12", "FL-4/13", "FL-4/14", "FL-4/15", 
        "FL-4/16", "FL-4/17", "FL-4/18", "FL-4/19", "FL-4/20", "FL-4/21", "FL-4/22", 
        "FL-4/23", "FL-4/24", "FL-4/25", "FL-4/26"
    ],
    "Saída_mm": [
        0.66, 0.91, 1.1, 1.3, 1.4, 1.6, 1.8, 2.0, 2.4, 2.8, 3.6, 4.0, 4.4, 
        4.8, 5.2, 6.4, 6.7, 7.5, 8.7, 12.7, 13.1, 13.9, 15.9, 18.3, 22.6, 26.2
    ],
    # Pressões em kg/cm²: 0.5, 1, 2, 3, 4, 5, 6, 7, 10, 20, 35
    0.5: [0.23, 0.48, 0.37, 0.50, 0.62, 0.75, 1.0, 1.2, 1.9, 2.5, 3.7, 5.0, 6.2, 7.5, 8.7, 12.5, 15.0, 18.7, 25.0, 50.0, 62.0, 72.0, 94.0, 125.0, 187.0, 250.0],
    1.0: [0.32, 0.64, 0.68, 0.91, 1.1, 1.4, 1.8, 2.3, 3.4, 4.6, 6.8, 9.1, 11.4, 13.7, 16.0, 23.0, 27.0, 34.0, 46.0, 91.0, 114.0, 132.0, 171.0, 230.0, 340.0, 480.0],
    2.0: [0.39, 0.79, 0.97, 1.3, 1.6, 1.9, 2.6, 3.2, 4.8, 6.5, 9.7, 12.9, 16.1, 19.3, 23.0, 32.0, 39.0, 48.0, 64.0, 129.0, 161.0, 187.0, 240.0, 325.0, 485.0, 650.0],
    3.0: [0.46, 0.91, 1.2, 1.6, 2.0, 2.4, 3.2, 3.9, 5.9, 7.9, 11.8, 15.8, 19.7, 24.0, 28.0, 39.0, 47.0, 59.0, 79.0, 158.0, 197.0, 230.0, 295.0, 395.0, 600.0, 790.0],
    4.0: [0.51, 1.0, 1.4, 1.8, 2.3, 2.7, 3.6, 4.6, 6.8, 9.1, 13.7, 18.2, 23.0, 27.0, 32.0, 46.0, 55.0, 68.0, 91.0, 182.0, 230.0, 265.0, 340.0, 455.0, 690.0, 910.0],
    5.0: [0.56, 1.1, 1.5, 2.0, 2.5, 3.1, 4.1, 5.1, 7.6, 10.2, 15.3, 20.0, 25.0, 31.0, 38.0, 51.0, 61.0, 76.0, 102.0, 205.0, 255.0, 295.0, 385.0, 510.0, 770.0, 1020.0],
    6.0: [0.60, 1.2, 1.7, 2.2, 2.8, 3.3, 4.5, 5.6, 8.4, 11.2, 16.7, 22.0, 28.0, 33.0, 39.0, 56.0, 67.0, 84.0, 112.0, 225.0, 280.0, 325.0, 420.0, 560.0, 840.0, 1120.0],
    7.0: [0.72, 1.4, 1.8, 2.4, 3.0, 3.6, 4.8, 6.0, 9.0, 12.1, 18.1, 24.0, 30.0, 36.0, 42.0, 60.0, 72.0, 90.0, 121.0, 240.0, 300.0, 350.0, 455.0, 610.0, 910.0, 1210.0],
    10.0: [1.0, 2.0, 2.2, 2.9, 3.8, 4.3, 5.8, 7.2, 10.8, 14.4, 22.0, 29.0, 36.0, 43.0, 50.0, 72.0, 86.0, 108.0, 144.0, 290.0, 360.0, 420.0, 540.0, 720.0, 1080.0, 1440.0],
    20.0: [1.3, 2.7, 3.1, 4.1, 5.1, 6.1, 8.2, 10.2, 15.3, 20.0, 31.0, 41.0, 51.0, 61.0, 71.0, 102.0, 122.0, 153.0, 205.0, 410.0, 510.0, 600.0, 770.0, 1020.0, 1530.0, 2040.0],
    35.0: [1.8, 3.5, 4.0, 5.4, 8.7, 8.1, 10.8, 13.5, 20.0, 27.0, 40.0, 54.0, 68.0, 81.0, 94.0, 135.0, 162.0, 205.0, 270.0, 540.0, 680.0, 780.0, 1010.0, 1350.0, 2020.0, 2700.0]
}

df_vazao = pd.DataFrame(dados_vazao)

# SEÇÃO DE PARÂMETROS
st.sidebar.header("Parâmetros do Chuveiro")

modelo_sel = st.sidebar.selectbox("Selecione o Modelo do Bico", df_vazao["Modelo"])
pressao_sel = st.sidebar.select_slider("Pressão de Operação (kg/cm²)", options=[0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 10.0, 20.0, 35.0], value=5.0)

num_bicos = st.sidebar.number_input("Quantidade de Bicos no Chuveiro", value=32, step=1)
horas_dia = st.sidebar.slider("Horas de Operação por Dia", min_value=1, max_value=24, value=24)
custo_m3 = st.sidebar.number_input("Custo da Água (R$ por m³)", value=4.50, step=0.50)

# BUSCAR VAZÃO NA TABELA
linha_bico = df_vazao[df_vazao["Modelo"] == modelo_sel].iloc[0]
vazao_un_lmin = linha_bico[pressao_sel]
saida_mm = linha_bico["Saída_mm"]

# CÁLCULOS TÉCNICOS
vazao_total_lmin = vazao_un_lmin * num_bicos
vazao_total_m3h = (vazao_total_lmin * 60) / 1000.0
consumo_diario_m3 = vazao_total_m3h * horas_dia
consumo_mensal_m3 = consumo_diario_m3 * 30
custo_mensal_brl = consumo_mensal_m3 * custo_m3

# EXIBIÇÃO DE RESULTADOS
st.subheader("📊 Resultados do Dimensionamento")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Diâmetro de Saída", f"{saida_mm} mm")
col2.metric("Vazão por Bico", f"{vazao_un_lmin} L/min")
col3.metric("Vazão Total Chuveiro", f"{vazao_total_lmin:.1f} L/min")
col4.metric("Vazão em m³/h", f"{vazao_total_m3h:.2f} m³/h")

st.divider()

st.subheader("💰 Impacto Financeiro e Consumo")
c1, c2, c3 = st.columns(3)
c1.metric("Consumo Diário", f"{consumo_diario_m3:.1f} m³")
c2.metric("Consumo Mensal (30 dias)", f"{consumo_mensal_m3:.1f} m³")
c3.metric("Custo Estimado Mensal", f"R$ {custo_mensal_brl:,.2f}")

# SIMULAÇÃO DE EFICIÊNCIA VOGON
st.divider()
st.subheader("🌱 Oportunidade de Otimização Vogon")
st.write("Sistemas de chuveiros Vogon com oscilação de alta precisão e bicos autolimpantes permitem substituir a vazão contínua por ciclos otimizados.")

economia_perc = st.slider("Percentual de Redução Esperado com Tecnologia Vogon (%)", 5, 30, 15)
economia_m3_mes = consumo_mensal_m3 * (economia_perc / 100.0)
economia_brl_mes = custo_mensal_brl * (economia_perc / 100.0)

st.success(f"💡 **Economia Estimada Vogon:** Redução de **{economia_m3_mes:.1f} m³/mês** de água, gerando uma economia financeira direta de **R$ {economia_brl_mes:,.2f} / mês**.")

# BOTÃO DE MEMÓRIA DE CÁLCULO
if st.button("Copiar Memória de Cálculo para Proposta"):
    st.code(f"""
=== MEMÓRIA DE CÁLCULO - CHUVEIRO VOGON GROUP ===
Modelo do Bico: {modelo_sel} (Ø Saída: {saida_mm} mm)
Pressão de Operação: {pressao_sel} kg/cm²
Quantidade de Bicos: {num_bicos}
Vazão Unitária: {vazao_un_lmin} L/min
Vazão Total da Linha: {vazao_total_lmin:.1f} L/min ({vazao_total_m3h:.2f} m³/h)
Consumo Mensal Estimado: {consumo_mensal_m3:.1f} m³
Custo Mensal Estimado: R$ {custo_mensal_brl:,.2f}
    """, language="text")
