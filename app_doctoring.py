import streamlit as st
import pandas as pd

# URL da Logo da Vogon Group
LOGO_URL = "https://yata-apix-320e5167-9d0d-4143-a25a-28eeb06af758.s3-object.locaweb.com.br/e88068311e2a46c2a3e029206757eb75.png"

st.set_page_config(
    page_title="Vogon Group - Doctoring system Specialist",
    page_icon=LOGO_URL,
    layout="wide"
)

# Estilização Vogon
st.markdown("""
    <style>
    .vogon-header { font-size: 22px; font-weight: bold; color: #0E2F56; }
    .stButton>button { background-color: #0E2F56; color: white; border-radius: 6px; }
    .card-box { background-color: #F4F6F9; padding: 20px; border-radius: 8px; border-left: 5px solid #0E2F56; }
    .photo-label { font-size: 13px; font-weight: bold; color: #0E2F56; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# CABEÇALHO
c_logo, c_title = st.columns([1, 3])
with c_logo:
    st.image(LOGO_URL, use_container_width=True)
with c_title:
    st.title("Vogon Group — Doctoring Specialist")
    st.caption("Sistema de Diagnóstico de Raspagem, Especificação e Relatório de Campo")

st.divider()

# MENUS DE SELEÇÃO NO SIDEBAR
st.sidebar.header("1. Identificação do Cliente & Máquina")
cliente = st.sidebar.text_input("Nome do Cliente / Usina", value="Klabin / Suzano")
maquina = st.sidebar.text_input("Identificação da Máquina", value="MP-01")
tecnico = st.sidebar.text_input("Técnico / Responsável Vogon", value="Eng. Vogon")

st.sidebar.divider()
st.sidebar.header("2. Posição de Instalação")
tipo_papel = st.sidebar.selectbox("Tipo de Papel", ["Papel Plano (Embalagem/E&I/Cartão)", "Papel Tissue (Higiênico/Toalha)"])

if tipo_papel == "Papel Plano (Embalagem/E&I/Cartão)":
    posicao = st.sidebar.selectbox("Posição na Máquina", [
        "Mesa Formadora / Rolo de Retorno",
        "Prensar / Rolo de Sucção / Prensa Central",
        "Secadores / Cilindro Secador",
        "Calandra / Enroladeira (Pope)"
    ])
else:
    posicao = st.sidebar.selectbox("Posição na Máquina", [
        "Cilindro Yankee - Lâmina de Crepagem",
        "Cilindro Yankee - Lâmina de Limpeza",
        "Rolo Prensa Suction / Blind Hole",
        "Rolo de Guia de Tela / Feltro"
    ])

# BASE DE DADOS TÉCNICA E SUGESTÕES DE LÂMINAS
def obter_dados_tecnicos(tipo, pos):
    if "Formadora" in pos or "Tela" in pos:
        return {
            "angulo": "20° a 25°",
            "pressao": "100 a 200 N/m (1.0 a 2.0 bar)",
            "lamina_mat": "Sintética (UHMW / Fibra de Vidro Epoxy)",
            "laminas_5": [
                "1. Vogon Poly-Clean UHMW (Sintética)",
                "2. Vogon Glass-Flex (Fibra de Vidro)",
                "3. Clouth KG-Master / Bonetti Lamcoat",
                "4. Kadant Synthetic-Pro",
                "5. Lantier Glass-Doctor"
            ],
            "dicas": "Verificar desgaste do rolo. Evitar lâminas metálicas nesta posição para não danificar o revestimento de borracha/PU."
        }
    elif "Prensar" in pos or "Prensa" in pos:
        return {
            "angulo": "23° a 28°",
            "pressao": "200 a 350 N/m (2.0 a 3.5 bar)",
            "lamina_mat": "Bronze Fosforoso / Aço Inox / Composta Cerâmica",
            "laminas_5": [
                "1. Vogon Bronze-Pro (Bronze Fosforoso)",
                "2. Vogon Inox-Flex 316L",
                "3. Bonetti Bronze-Master / Clouth Polybronze",
                "4. Kadant VeriLite / Oradoc Bronze",
                "5. Essco Bronzite / Huatao Bronze-Edge"
            ],
            "dicas": "Checar alinhamento do porta-lâminas DST. Limpeza periódica dos bicos de chuveiro para evitar impregnação de fita de massa."
        }
    elif "Secador" in pos:
        return {
            "angulo": "25° a 30°",
            "pressao": "150 a 250 N/m (1.5 a 2.5 bar)",
            "lamina_mat": "Aço Carbono Temperado / Fibra de Carbono",
            "laminas_5": [
                "1. Vogon Carbon-Steel Hi-Ten",
                "2. Vogon Carbo-Flex (Fibra de Carbono)",
                "3. Clouth Galena / Bonetti Steel-Max",
                "4. Kadant ProSteel / Essco Steel-Edge",
                "5. Lantier Carbo-Line / Huatao Steel"
            ],
            "dicas": "Verificar oscilação mecânica/pneumática. A falta de oscilação causa riscos e sulcos no cilindro secador."
        }
    elif "Crepagem" in pos:
        return {
            "angulo": "16° a 22° (Ângulo de Contato)",
            "pressao": "250 a 450 N/m (2.5 a 4.5 bar)",
            "lamina_mat": "Aço Carbono Especial / Carbeto de Tungstênio / Cerâmica",
            "laminas_5": [
                "1. Vogon Crepe-Master Tungsten (Carbeto)",
                "2. Vogon Crepe-Steel Premium",
                "3. Bonetti Crepe-Edge / Clouth Creper",
                "4. Kadant CeraFlex / Oradoc Ceramic",
                "5. Joh. Clouth SuperCrepe / Essco CeramiCrepe"
            ],
            "dicas": "Monitorar o ângulo do bisel (bevel) da lâmina e a espessura do filme químico (coating). Mantenha o oscilador ativo."
        }
    else:
        return {
            "angulo": "25° a 28°",
            "pressao": "200 a 300 N/m (2.0 a 3.0 bar)",
            "lamina_mat": "Aço Inox / Revestimento Cerâmico",
            "laminas_5": [
                "1. Vogon Inox-Precision",
                "2. Vogon Cera-Shield",
                "3. Clouth Stainless / Bonetti Inox",
                "4. Kadant VeriDur / Oradoc Inox",
                "5. Lantier Stainless-Pro"
            ],
            "dicas": "Inspecionar mangueiras pneumáticas do porta-lâminas e travas do tubo oscilante."
        }

dados_pos = obter_dados_tecnicos(tipo_papel, posicao)

# EXIBIÇÃO DO PAINEL DE ENGENHARIA DE RASPAGEM
st.subheader("⚙️ Parâmetros Recomendados de Operação")

col_a, col_b, col_c = st.columns(3)
col_a.metric("Ângulo Ideal de Raspagem", dados_pos["angulo"])
col_b.metric("Pressão Linear Recomendada", dados_pos["pressao"])
col_c.metric("Material Base Indicado", dados_pos["lamina_mat"])

st.info(f"💡 **Sugestões de Melhoria Vogon:** {dados_pos['dicas']}")

st.divider()

# SELEÇÃO DE LÂMINAS DE MERCADO (BENCHMARKING)
st.subheader("🔪 Lâminas Compatíveis & Equivalência de Mercado")
for lam in dados_pos["laminas_5"]:
    st.write(f"- {lam}")

st.divider()

# REGISTRO FOTOGRÁFICO DE CAMPO (4 FOTOS)
st.subheader("📸 Registro Fotográfico do Ajuste de Ângulos (LA / LC)")
st.write("Anexe as imagens capturadas em campo pelo iPhone/iPad para comprovação técnica:")

st.markdown("#### 🔴 1. Fotos ANTES do Ajuste")
col_antes_la, col_antes_lc = st.columns(2)

with col_antes_la:
    img_antes_la = st.file_uploader("Foto ANTES — Lado Acionamento (LA)", type=["png", "jpg", "jpeg"], key="u_antes_la")
    if img_antes_la:
        st.image(img_antes_la, caption="ANTES — Lado Acionamento (LA)", use_container_width=True)

with col_antes_lc:
    img_antes_lc = st.file_uploader("Foto ANTES — Lado Comando (LC)", type=["png", "jpg", "jpeg"], key="u_antes_lc")
    if img_antes_lc:
        st.image(img_antes_lc, caption="ANTES — Lado Comando (LC)", use_container_width=True)

st.markdown("#### 🟢 2. Fotos DEPOIS do Ajuste")
col_depois_la, col_depois_lc = st.columns(2)

with col_depois_la:
    img_depois_la = st.file_uploader("Foto DEPOIS — Lado Acionamento (LA)", type=["png", "jpg", "jpeg"], key="u_depois_la")
    if img_depois_la:
        st.image(img_depois_la, caption="DEPOIS — Lado Acionamento (LA)", use_container_width=True)

with col_depois_lc:
    img_depois_lc = st.file_uploader("Foto DEPOIS — Lado Comando (LC)", type=["png", "jpg", "jpeg"], key="u_depois_lc")
    if img_depois_lc:
        st.image(img_depois_lc, caption="DEPOIS — Lado Comando (LC)", use_container_width=True)

st.divider()

# FORMULÁRIO DE INTERVENÇÃO
st.subheader("📝 Detalhes da Intervenção Diária de Campo")

col_f1, col_f2 = st.columns(2)

with col_f1:
    servico_feito = st.text_area("O que foi FEITO hoje na intervenção?", value="Ajuste do ângulo do porta-lâminas DST, aferição da pressão e substituição da lâmina gasta.")
    pecas_substituidas = st.text_area("Peças SUBSTITUÍDAS hoje:", value="1x Lâmina Vogon Inox-Precision 4500mm;\n2x Mangueiras de acionamento pneumático.")

with col_f2:
    falta_fazer = st.text_area("O que FALTA FAZER / Pendências:", value="Acompanhar alinhamento no próximo arranque da fábrica.")
    pecas_providenciar = st.text_area("Peças a serem PROVIDENCIADAS / Cotar:", value="1x Kit de vedação do tubo oscilante.")

# GERADOR DE DOCUMENTO FINAL TIMBRADO
st.divider()
if st.button("📄 Gerar Relatório Completo com Fotos"):
    st.subheader("📄 RELATÓRIO TÉCNICO DE INTERVENÇÃO - VOGON GROUP")
    
    st.markdown(f"""
    <div class="card-box">
    <div style="text-align: center;">
        <h2 style="color: #0E2F56; margin-bottom: 2px;">VOGON GROUP LTDA</h2>
        <p style="font-size: 12px; margin-top: 0px;">
        MATRIZ: 42.730.025/0001-90 | FILIAL: 42.730.025/0002-71<br>
        Av. Guilherme George, 1364 - Jundiapeba, Mogi das Cruzes - SP, 08750-540<br>
        (11) 97637-8235 | WWW.VOGONGROUP.COM.BR
        </p>
    </div>
    <hr>
    <p><b>CLIENTE:</b> {cliente} | <b>MÁQUINA:</b> {maquina}</p>
    <p><b>RESPONSÁVEL TÉCNICO:</b> {tecnico}</p>
    <p><b>POSIÇÃO AVALIADA:</b> {posicao} ({tipo_papel})</p>
    <hr>
    <h4>1. PARÂMETROS TÉCNICOS CONFIGURADOS:</h4>
    <ul>
        <li><b>Ângulo Definido:</b> {dados_pos['angulo']}</li>
        <li><b>Pressão de Trabalho:</b> {dados_pos['pressao']}</li>
        <li><b>Material da Lâmina:</b> {dados_pos['lamina_mat']}</li>
    </ul>
    
    <h4>2. ATIVIDADES REALIZADAS & PEÇAS:</h4>
    <p><b>Serviço Concluído:</b><br>{servico_feito}</p>
    <p><b>Peças Substituídas:</b><br>{pecas_substituidas}</p>

    <h4>3. PENDÊNCIAS & PROVEDORIA:</h4>
    <p><b>Ações Pendentes:</b><br>{falta_fazer}</p>
    <p><b>Peças a Providenciar:</b><br>{pecas_providenciar}</p>
    </div>
    """, unsafe_allow_html=True)

    # REPOSITÓRIO VISUAL NO RELATÓRIO
    st.markdown("### 📸 Evidências Fotográficas do Ajuste de Ângulos")
    
    rc1, rc2 = st.columns(2)
    with rc1:
        st.caption("🔴 **ANTES — Lado Acionamento (LA)**")
        if img_antes_la:
            st.image(img_antes_la, use_container_width=True)
        else:
            st.write("*(Foto não anexada)*")

        st.caption("🟢 **DEPOIS — Lado Acionamento (LA)**")
        if img_depois_la:
            st.image(img_depois_la, use_container_width=True)
        else:
            st.write("*(Foto não anexada)*")

    with rc2:
        st.caption("🔴 **ANTES — Lado Comando (LC)**")
        if img_antes_lc:
            st.image(img_antes_lc, use_container_width=True)
        else:
            st.write("*(Foto não anexada)*")

        st.caption("🟢 **DEPOIS — Lado Comando (LC)**")
        if img_depois_lc:
            st.image(img_depois_lc, use_container_width=True)
        else:
            st.write("*(Foto não anexada)*")

    st.caption("Documento gerado via Vogon Doctoring Specialist App — Tecnologia Industrial Vogon Group.")
