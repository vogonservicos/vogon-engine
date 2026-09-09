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
    .alert-box { background-color: #FFEBEE; padding: 15px; border-radius: 8px; border-left: 5px solid #C62828; margin-bottom: 15px; }
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
    st.caption("Sistema de Diagnóstico, Validação de Tolerâncias e Histórico em Excel")

st.divider()

# 1. IDENTIFICAÇÃO DO CLIENTE & MÁQUINA
st.sidebar.header("1. Identificação Geral")
cliente = st.sidebar.text_input("Nome do Cliente / Usina", value="Klabin")
maquina = st.sidebar.text_input("Identificação da Máquina", value="MP-01")
data_hoje = st.sidebar.date_input("Data da Intervenção", datetime.today())
tecnico = st.sidebar.text_input("Técnico / Responsável Vogon", value="Eng. Vogon")

st.sidebar.divider()

# 2. POSIÇÃO DE INSTALAÇÃO
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

# CAMPO DE POSIÇÃO DETALHADA
posicao_detalhada = st.sidebar.text_input(
    "Posição Exata da Intervenção", 
    value="Cilindro Secador 78",
    help="Ex: Rolo superior 4ª prensa, Cilindro Secador 78, Rolo de Sucção 1"
)

# REGRAS TÉCNICAS E AMARRAÇÃO DE RANGE DE TOLERÂNCIA (ATÉ 32 GRAUS AMPLIOU)
def obter_regras_engenharia(grupo):
    if "Formadora" in grupo:
        return {"ang_min": 20, "ang_max": 25, "press_max": 200, "ref_ang": "20° a 25°", "ref_press": "100 a 200 N/m", "mat": "Sintética (UHMW / Epoxy)"}
    elif "Prensar" in grupo:
        return {"ang_min": 23, "ang_max": 32, "press_max": 350, "ref_ang": "23° a 32°", "ref_press": "200 a 350 N/m", "mat": "Bronze / Inox / Cerâmica"}
    elif "Secador" in grupo:
        return {"ang_min": 25, "ang_max": 32, "press_max": 250, "ref_ang": "25° a 32°", "ref_press": "150 a 250 N/m", "mat": "Aço Carbono / Fibra de Carbono"}
    elif "Yankee" in grupo:
        return {"ang_min": 16, "ang_max": 22, "press_max": 450, "ref_ang": "16° a 22°", "ref_press": "250 a 450 N/m", "mat": "Carbeto de Tungstênio / Cerâmica"}
    else: # Calandra / Enroladeira
        return {"ang_min": 25, "ang_max": 32, "press_max": 300, "ref_ang": "25° a 32°", "ref_press": "200 a 300 N/m", "mat": "Aço Inox / Cerâmica"}

regras = obter_regras_engenharia(grupo_posicao)

# EXIBIÇÃO DE PARÂMETROS PADRÃO
st.subheader(f"📍 Posição Selecionada: {posicao_detalhada}")
col_a, col_b, col_c = st.columns(3)
col_a.metric("Ângulo Tolera (Range Max)", regras["ref_ang"])
col_b.metric("Pressão Limite Máxima", regras["ref_press"])
col_c.metric("Material Indicado", regras["mat"])

st.divider()

# 3. VALIDAÇÃO DE ÂNGULO E PRESSÃO EM CAMPO
st.subheader("⚙️ Aferição de Ângulo e Pressão Ajustados")

col_input1, col_input2 = st.columns(2)

with col_input1:
    angulo_ajustado = st.number_input("Ângulo Real Ajustado na Viga (°)", value=float(regras["ang_min"]), step=0.5)
with col_input2:
    pressao_ajustada = st.number_input("Pressão Real Aplicada (N/m)", value=200.0, step=10.0)

# LÓGICA DE DETECÇÃO DE DESVIO / ALERTA
fora_do_range_angulo = (angulo_ajustado < regras["ang_min"]) or (angulo_ajustado > regras["ang_max"])
fora_do_range_pressao = pressao_ajustada > regras["press_max"]
necessita_aprovacao = fora_do_range_angulo or fora_do_range_pressao

aprovador_nome = ""
if necessita_aprovacao:
    st.markdown(f"""
    <div class="alert-box">
        <h4 style="color: #C62828; margin-top:0px;">⚠️ ATENÇÃO: PARÂMETROS FORA DA TABELA DE TOLERÂNCIA DE ENGENHARIA!</h4>
        <p>O ângulo configurado (<b>{angulo_ajustado}°</b>) ou a pressão (<b>{pressao_ajustada} N/m</b>) ultrapassam os limites padrão para esta seção ({regras['ref_ang']} / {regras['ref_press']}).</p>
        <p><b>A gravação na planilha requer APROVAÇÃO OBRIGATÓRIA do Gestor Vogon ou do Cliente responsável.</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    aprovador_nome = st.text_input("👤 Nome e Cargo do Aprovador (Cliente ou Gestor):", help="Ex: Eng. Carlos - Gerente de Manutenção Klabin")
else:
    st.success("✅ **Parâmetros Operacionais Válidos:** Dentro da faixa de tolerância autorizada.")

st.divider()

# 4. ESPECIFICAÇÃO DA LÂMINA INSTALADA
st.subheader("🔪 Especificação Técnica da Lâmina Instalada")

c_lam1, c_lam2 = st.columns(2)

with c_lam1:
    lamina_nome = st.text_input("Modelo / Código da Lâmina Instalada", value="Vogon Inox-Precision")
    lamina_material = st.selectbox(
        "Material da Lâmina Instalada",
        ["Aço Inox 304/316L", "Aço Carbono Temperado", "Bronze Fosforoso", "Sintética / UHMW", "Fibra de Vidro", "Fibra de Carbono", "Carbeto de Tungstênio / Cerâmica", "Outro"]
    )

with c_lam2:
    tipo_rebitagem = st.selectbox(
        "Tipo de Rebitagem",
        ["DST", "KF", "DSTF", "KF Frontal", "A1", "Conformatic", "Sem Rebites", "Outros"]
    )
    if tipo_rebitagem == "Outros":
        rebitagem_detalhe = st.text_input("Especifique o Tipo de Rebitagem:", value="Padrão Especial Vogon")
    else:
        rebitagem_detalhe = tipo_rebitagem

st.markdown("##### 📐 Dimensões Geométricas da Lâmina (em milímetros)")
c_dim1, c_dim2, c_dim3 = st.columns(3)

with c_dim1:
    lam_largura = st.number_input("Largura (mm)", value=76.2, step=1.0)
with c_dim2:
    lam_espessura = st.number_input("Espessura (mm)", value=1.20, step=0.05, format="%.2f")
with c_dim3:
    lam_comprimento = st.number_input("Comprimento (mm)", value=4500.0, step=10.0)

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
    servico_feito = st.text_area("Serviço Realizado:", value="Ajuste do ângulo de ataque, verificação de pressão e troca de lâmina gasta.")
    pecas_substituidas = st.text_area("Peças Substituídas:", value=f"1x Lâmina {lamina_nome} ({lam_largura}x{lam_espessura}x{lam_comprimento} mm) Rebitagem {rebitagem_detalhe}.")
with c_f2:
    falta_fazer = st.text_area("Pendências / Falta Fazer:", value="Monitorar limpeza do tubo na próxima parada.")
    pecas_providenciar = st.text_area("Peças a Providenciar:", value="1x Kit de vedação de suporte.")

# BOTÃO PARA ADICIONAR REGISTRO À PLANILHA DO DIA (COM VALIDAÇÃO DE BLOQUEIO)
st.divider()

# DESABILITA O BOTÃO SE HOUVER DESVIO SEM NOMINAR APROVADOR
bloquear_botao = necessita_aprovacao and (len(aprovador_nome.strip()) == 0)

if bloquear_botao:
    st.warning("🔒 **Ação Bloqueada:** Preencha o campo **'Nome e Cargo do Aprovador'** acima para permitir a gravação desta intervenção.")

if st.button("➕ Salvar Registro desta Posição na Planilha do Dia", disabled=bloquear_botao):
    status_aprovacao_txt = f"APROVADO POR: {aprovador_nome}" if necessita_aprovacao else "DENTRO DO PADRÃO ENGENHARIA"
    
    registro = {
        "Data": data_hoje.strftime("%d/%m/%Y"),
        "Cliente": cliente,
        "Máquina": maquina,
        "Técnico": tecnico,
        "Tipo Papel": tipo_papel,
        "Seção": grupo_posicao,
        "Posição Exata (Raspador)": posicao_detalhada,
        "Ângulo Real Ajustado (°)": angulo_ajustado,
        "Pressão Real Aplicada (N/m)": pressao_ajustada,
        "Status Tolerância": "FORA DO PADRÃO (APROVADO)" if necessita_aprovacao else "PADRÃO OK",
        "Aprovador Responsável": status_aprovacao_txt,
        "Lâmina Instalada": lamina_nome,
        "Material Lâmina": lamina_material,
        "Largura (mm)": lam_largura,
        "Espessura (mm)": lam_espessura,
        "Comprimento (mm)": lam_comprimento,
        "Dimensão Total (LxExC mm)": f"{lam_largura} x {lam_espessura} x {lam_comprimento}",
        "Tipo Rebitagem": rebitagem_detalhe,
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
    st.success(f"✅ Intervenção na posição **'{posicao_detalhada}'** gravada! Status: **{status_aprovacao_txt}**")

# EXIBIÇÃO DA TABELA DO DIA E EXPORTAÇÃO EXCEL
if len(st.session_state['historico_intervencao']) > 0:
    st.divider()
    st.subheader("📊 Histórico de Intervenções Acumuladas Hoje")
    
    df_historico = pd.DataFrame(st.session_state['historico_intervencao'])
    
    # Exibição resumida na tela
    colunas_visiveis = ["Data", "Cliente", "Máquina", "Posição Exata (Raspador)", "Ângulo Real Ajustado (°)", "Status Tolerância", "Aprovador Responsável", "Lâmina Instalada"]
    st.dataframe(df_historico[colunas_visiveis], use_container_width=True)

    # NOME DO ARQUIVO SEGUINDO O PADRÃO (por dia, por máquina, por cliente)
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
