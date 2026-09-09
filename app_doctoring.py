import streamlit as st
import pandas as pd
from datetime import datetime
import io

# URL da Logo da Vogon Group
LOGO_URL = "https://yata-apix-320e5167-9d0d-4143-a25a-28eeb06af758.s3-object.locaweb.com.br/e88068311e2a46c2a3e029206757eb75.png"

st.set_page_config(
    page_title="Vogon Group - Doctoring Specialist",
    page_icon=LOGO_URL,
    layout="wide"
)

# Estilização Vogon
st.markdown("""
    <style>
    .vogon-header { font-size: 22px; font-weight: bold; color: #0E2F56; }
    .stButton>button { background-color: #0E2F56; color: white; border-radius: 6px; }
    .card-box { background-color: #F4F6F9; padding: 20px; border-radius: 8px; border-left: 5px solid #0E2F56; }
    </style>
""", unsafe_allow_html=True)

# INICIALIZAR PLANILHA/BANCO NA SESSÃO DO APP
if 'historico_intervencao' not in st.session_state:
    st.session_state['historico_intervencao'] = []

# CABEÇALHO
c_logo, c_title = st.columns([1, 3])
with c_logo:
    st.image(LOGO_URL, use_container_width=True)
with c_title:
    st.title("Vogon Group — Doctoring Specialist")
    st.caption("Sistema de Diagnóstico, Registro Fotográfico e Histórico em Excel")

st.divider()

# 1. IDENTIFICAÇÃO DO CLIENTE & MÁQUINA
st.sidebar.header("1. Identificação Geral")
cliente = st.sidebar.text_input("Nome do Cliente / Usina", value="Klabin")
maquina = st.sidebar.text_input("Identificação da Máquina", value="MP-01")
data_hoje = st.sidebar.date_input("Data da Intervenção", datetime.today())
tecnico = st.sidebar.text_input("Técnico / Responsável Vogon", value="Eng. Vogon")

st.sidebar.divider()

# 2. POSIÇÃO DE INSTALAÇÃO E ESPECIFICAÇÃO
st.sidebar.header("2. Posição da Máquina & Intervenção")
tipo_papel = st.sidebar.selectbox("Tipo de Papel", ["Papel Plano (Embalagem/E&I/Cartão)", "Papel Tissue (Higiênico/Toalha)"])

if tipo_papel == "Papel Plano (Embalagem/E&I/Cartão)":
    grupo_posicao = st.sidebar.selectbox("Seção da Máquina", [
        "Mesa Formadora / Rolo de Retorno",
        "Prensar / Rolo de Sucção / Prensa Central",
        "Secadores / Cilindros Secadores",
        "Calandra / Enroladeira (Pope)"
    ])
else:
    grupo_posicao = st.sidebar.selectbox("Seção da Máquina", [
        "Cilindro Yankee - Crepagem / Limpeza",
        "Rolo Prensa Suction / Blind Hole",
        "Rolo de Guia de Tela / Feltro"
    ])

# CAMPO DE POSIÇÃO DETALHADA / ESPECÍFICA (Solicitado pelo usuário)
posicao_detalhada = st.sidebar.text_input(
    "Posição Exata da Intervenção", 
    value="Cilindro Secador 78",
    help="Ex: Rolo superior 4ª prensa, Cilindro Secador 78, Rolo de Sucção 1"
)

# REGRAS TÉCNICAS E LÂMINAS
def obter_dados_tecnicos(grupo):
    if "Formadora" in grupo:
        return {"angulo": "20° a 25°", "pressao": "100 a 200 N/m", "mat": "Sintética (UHMW / Epoxy)"}
    elif "Prensar" in grupo:
        return {"angulo": "23° a 28°", "pressao": "200 a 350 N/m", "mat": "Bronze / Inox / Cerâmica"}
    elif "Secador" in grupo:
        return {"angulo": "25° a 30°", "pressao": "150 a 250 N/m", "mat": "Aço Carbono / Fibra de Carbono"}
    elif "Yankee" in grupo:
        return {"angulo": "16° a 22°", "pressao": "250 a 450 N/m", "mat": "Carbeto de Tungstênio / Cerâmica"}
    else:
        return {"angulo": "25° a 28°", "pressao": "200 a 300 N/m", "mat": "Aço Inox / Cerâmica"}

dados_pos = obter_dados_tecnicos(grupo_posicao)

# EXIBIÇÃO DE PARÂMETROS
st.subheader(f"📍 Posição Selecionada: {posicao_detalhada}")
col_a, col_b, col_c = st.columns(3)
col_a.metric("Ângulo Ideal", dados_pos["angulo"])
col_b.metric("Pressão Recomendada", dados_pos["pressao"])
col_c.metric("Material Indicado", dados_pos["mat"])

st.divider()

# REGISTRO FOTOGRÁFICO DE CAMPO
st.subheader("📸 Fotos do Ajuste de Ângulos (LA / LC)")
col1, col2 = st.columns(2)
with col1:
    img_antes_la = st.file_uploader("Foto ANTES — Lado Acionamento (LA)", type=["jpg", "jpeg", "png"], key="la_a")
    img_depois_la = st.file_uploader("Foto DEPOIS — Lado Acionamento (LA)", type=["jpg", "jpeg", "png"], key="la_d")
with col2:
    img_antes_lc = st.file_uploader("Foto ANTES — Lado Comando (LC)", type=["jpg", "jpeg", "png"], key="lc_a")
    img_depois_lc = st.file_uploader("Foto DEPOIS — Lado Comando (LC)", type=["jpg", "jpeg", "png"], key="lc_d")

st.divider()

# CAMPOS DE DETALHAMENTO DA INTERVENÇÃO
st.subheader("📝 Detalhes do Serviço nesta Posição")
c_f1, c_f2 = st.columns(2)
with c_f1:
    servico_feito = st.text_area("Serviço Realizado:", value="Ajuste do ângulo de ataque, troca de mangueiras pneumáticas e substituição da lâmina.")
    pecas_substituidas = st.text_area("Peças Substituídas:", value="1x Lâmina Vogon Inox 4500mm.")
with c_f2:
    falta_fazer = st.text_area("Pendências / Falta Fazer:", value="Acompanhar desgaste em 15 dias.")
    pecas_providenciar = st.text_area("Peças a Providenciar:", value="1x Kit Reparo Cilindro Pneumático.")

# BOTÃO PARA ADICIONAR REGISTRO À PLANILHA DO DIA
st.divider()
if st.button("➕ Salvar Registro desta Posição na Planilha do Dia"):
    registro = {
        "Data": data_hoje.strftime("%d/%m/%Y"),
        "Cliente": cliente,
        "Máquina": maquina,
        "Técnico": tecnico,
        "Tipo Papel": tipo_papel,
        "Seção": grupo_posicao,
        "Posição Exata (Raspador)": posicao_detalhada,
        "Ângulo (Ajustado/Ref)": dados_pos["angulo"],
        "Pressão (Ajustada/Ref)": dados_pos["pressao"],
        "Material Lâmina": dados_pos["mat"],
        "Serviço Realizado": servico_feito,
        "Peças Substituídas": pecas_substituidas,
        "Pendências": falta_fazer,
        "Peças a Providenciar": pecas_providenciar,
        "Foto Antes LA": "Anexada" if img_antes_la else "Ausente",
        "Foto Depois LA": "Anexada" if img_depois_la else "Ausente",
        "Foto Antes LC": "Anexada" if img_antes_lc else "Ausente",
        "Foto Depois LC": "Anexada" if img_depois_lc else "Ausente"
    }
    st.session_state['historico_intervencao'].append(registro)
    st.success(f"✅ Intervenção na posição **'{posicao_detalhada}'** adicionada ao histórico de hoje!")

# EXIBIÇÃO DA TABELA DO DIA E EXPORTAÇÃO EXCEL
if len(st.session_state['historico_intervencao']) > 0:
    st.divider()
    st.subheader("📊 Histórico de Intervenções Acumuladas Hoje")
    
    df_historico = pd.DataFrame(st.session_state['historico_intervencao'])
    st.dataframe(df_historico[["Data", "Cliente", "Máquina", "Posição Exata (Raspador)", "Serviço Realizado", "Peças Substituídas"]], use_container_width=True)

    # NOME DO ARQUIVO SEGUINDO O PADRÃO (Sua regra: por dia, por máquina, por cliente)
    data_str = data_hoje.strftime("%Y-%m-%d")
    nome_arquivo_excel = f"Vogon_{cliente.replace(' ', '_')}_{maquina.replace(' ', '_')}_{data_str}.xlsx"

    # GERAR O ARQUIVO EXCEL EM MEMÓRIA
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_historico.to_excel(writer, index=False, sheet_name='Intervençoes_Vogon')
    processed_data = output.getvalue()

    st.download_button(
        label=f"📥 Baixar Planilha Excel Oficial ({nome_arquivo_excel})",
        data=processed_data,
        file_name=nome_arquivo_excel,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
