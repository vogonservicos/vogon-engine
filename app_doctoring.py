import streamlit as st
import pandas as pd
from datetime import datetime
import io
import urllib.parse
from fpdf import FPDF

# URL da Logo Oficial Vogon Group
LOGO_URL = "https://yata-apix-320e5167-9d0d-4143-a25a-28eeb06af758.s3-object.locaweb.com.br/e88068311e2a46c2a3e029206757eb75.png"

st.set_page_config(
    page_title="Vogon Group - Doctoring Specialist",
    page_icon=LOGO_URL,
    layout="wide"
)

# Estilização Visual Vogon
st.markdown("""
    <style>
    .vogon-header { font-size: 22px; font-weight: bold; color: #0E2F56; }
    .stButton>button { background-color: #0E2F56; color: white; border-radius: 6px; }
    .card-box { background-color: #F4F6F9; padding: 20px; border-radius: 8px; border-left: 5px solid #0E2F56; }
    .alert-box { background-color: #FFEBEE; padding: 15px; border-radius: 8px; border-left: 5px solid #C62828; margin-bottom: 15px; }
    .manager-box { background-color: #E3F2FD; padding: 15px; border-radius: 8px; border: 1px solid #90CAF9; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 🔒 1. BANCO DE DADOS DE GESTORES E TÉCNICOS
# ==============================================================================
USUARIOS_CADASTRADOS = {
    "jucieliorodrigues@vogongroup.com.br": {
        "nome": "Jucielio Rodrigues",
        "senha": "1008",
        "perfil": "gestor_master",
        "cargo": "Gestor Master / Direção",
        "primeiro_acesso": True
    },
    "izagomesrodrigues@vogongroup.com.br": {
        "nome": "Iza Gomes Rodrigues",
        "senha": "1008",
        "perfil": "gestor_master",
        "cargo": "Gestora Master / Direção",
        "primeiro_acesso": True
    },
    "rogeriomedeiros@vogongroup.com.br": {
        "nome": "Rogério Medeiros",
        "senha": "1008",
        "perfil": "gestor",
        "cargo": "Gestor de Operações",
        "primeiro_acesso": True
    },
    "tecnico.vogon@vogongroup.com.br": {
        "nome": "Técnico de Campo Vogon",
        "senha": "vogon2026@doctoring",
        "perfil": "tecnico",
        "cargo": "Especialista de Processo",
        "primeiro_acesso": False
    }
}

# GERENCIADOR DE SESSÃO
if 'logado' not in st.session_state:
    st.session_state['logado'] = False
if 'usuario_dados' not in st.session_state:
    st.session_state['usuario_dados'] = None
if 'usuario_id' not in st.session_state:
    st.session_state['usuario_id'] = None
if 'historico_intervencao' not in st.session_state:
    st.session_state['historico_intervencao'] = []

# TELA DE LOGIN
if not st.session_state['logado']:
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h2 style='color: #0E2F56; margin-bottom: 0px;'>VOGON GROUP LTDA</h2>
            <h4 style='color: #555; margin-top: 5px;'>Sistema Corporativo — Doctoring Specialist</h4>
            <p style='font-size: 14px; color: #777;'>Acesso restrito para equipe técnica e gestores autorizados.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_centered = st.columns([1, 2, 1])
    with col_centered[1]:
        with st.form("form_login_vogon"):
            st.subheader("🔑 Autenticação de Usuário")
            user_input = st.text_input("E-mail Corporativo").strip().lower()
            pass_input = st.text_input("Senha", type="password")
            btn_entrar = st.form_submit_button("Entrar no Sistema", use_container_width=True)
            
            if btn_entrar:
                if user_input in USUARIOS_CADASTRADOS and USUARIOS_CADASTRADOS[user_input]["senha"] == pass_input:
                    st.session_state['logado'] = True
                    st.session_state['usuario_id'] = user_input
                    st.session_state['usuario_dados'] = USUARIOS_CADASTRADOS[user_input]
                    st.rerun()
                else:
                    st.error("❌ E-mail ou senha incorretos.")
    st.stop()

# MODAL DE PRIMEIRO ACESSO
usr = st.session_state['usuario_dados']
usr_id = st.session_state['usuario_id']

if usr.get("primeiro_acesso", False):
    st.markdown("<h3 style='color: #C62828; text-align: center;'>🔒 Redefinição de Senha Obrigatória (1º Acesso)</h3>", unsafe_allow_html=True)
    st.info(f"Olá, **{usr['nome']}**! Por motivos de segurança corporativa Vogon, cadastre sua nova senha de acesso antes de prosseguir.")
    
    col_senha = st.columns([1, 2, 1])
    with col_senha[1]:
        with st.form("form_primeiro_acesso"):
            nova_senha = st.text_input("Digite sua Nova Senha (mínimo 4 dígitos)", type="password")
            confirma_senha = st.text_input("Confirme a Nova Senha", type="password")
            btn_salvar_senha = st.form_submit_button("Atualizar Senha e Acessar", use_container_width=True)
            
            if btn_salvar_senha:
                if len(nova_senha.strip()) < 4:
                    st.error("⚠️ A senha deve conter pelo menos 4 dígitos.")
                elif nova_senha != confirma_senha:
                    st.error("⚠️ As senhas digitadas não coincidem.")
                elif nova_senha == "1008":
                    st.error("⚠️ A nova senha não pode ser igual à senha provisória inicial (1008).")
                else:
                    USUARIOS_CADASTRADOS[usr_id]["senha"] = nova_senha
                    USUARIOS_CADASTRADOS[usr_id]["primeiro_acesso"] = False
                    st.session_state['usuario_dados']['primeiro_acesso'] = False
                    st.success("✅ Senha alterada com sucesso!")
                    st.rerun()
    st.stop()

# BARRA LATERAL
st.sidebar.markdown(f"""
    <div style='background-color: #E8EEF5; padding: 12px; border-radius: 6px; margin-bottom: 15px;'>
        <p style='margin: 0; font-size: 11px; color: #555;'>Usuário Autenticado:</p>
        <p style='margin: 0; font-weight: bold; color: #0E2F56;'>{usr['nome']}</p>
        <p style='margin: 0; font-size: 11px; color: #008000; font-weight: bold;'>{usr['cargo']}</p>
    </div>
""", unsafe_allow_html=True)

if st.sidebar.button("🚪 Sair do Sistema (Logout)", use_container_width=True):
    st.session_state['logado'] = False
    st.session_state['usuario_dados'] = None
    st.session_state['usuario_id'] = None
    st.rerun()

# ==============================================================================
# 📄 GERADOR DE PDF TIMBRADO VOGON
# ==============================================================================
def gerar_pdf_timbrado(reg):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho Fiscais Vogon
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(14, 47, 86)
    pdf.cell(0, 8, "VOGON GROUP LTDA", ln=True, align="C")
    
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, "CNPJ MATRIZ: 42.730.025/0001-90 | FILIAL: 42.730.025/0002-71", ln=True, align="C")
    pdf.cell(0, 5, "Av. Guilherme George, 1364 - Jundiapeba, Mogi das Cruzes - SP | (11) 97637-8235", ln=True, align="C")
    pdf.cell(0, 5, "WWW.VOGONGROUP.COM.BR", ln=True, align="C")
    pdf.line(10, 32, 200, 32)
    pdf.ln(8)
    
    # Título do Documento
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(14, 47, 86)
    pdf.cell(0, 7, f"RELATORIO TECNICO DE INTERVENCAO - {reg['Cliente']}", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, f"Data: {reg['Data']} | Maquina: {reg['Maquina']} | Tecnico: {reg['Tecnico Logado']}", ln=True)
    pdf.cell(0, 6, f"Posicao Avaliada: {reg['Posicao Exata (Raspador)']} ({reg['Tipo Papel']})", ln=True)
    pdf.ln(4)
    
    # Parametros
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, "1. PARAMETROS TECNICOS DE RASPAGEM:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5, f" - Angulo Ajustado: {reg['Angulo Real (°)']} deg | Pressao Aplicada: {reg['Pressao Real (N/m)']} N/m", ln=True)
    pdf.cell(0, 5, f" - Status de Tolerancia: {reg['Status Tolerancia']}", ln=True)
    pdf.cell(0, 5, f" - Responsavel Aprovacao: {reg['Aprovador Responsavel']}", ln=True)
    pdf.ln(4)
    
    # Lamina
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, "2. ESPECIFICACAO DA LAMINA INSTALADA:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5, f" - Modelo/Material: {reg['Lamina Instalada']} ({reg['Material Lamina']})", ln=True)
    pdf.cell(0, 5, f" - Dimensoes (LxExC): {reg['Dimensao Total (LxExC mm)']} mm", ln=True)
    pdf.cell(0, 5, f" - Tipo de Rebitagem: {reg['Tipo Rebitagem']}", ln=True)
    pdf.ln(4)

    # Servico e Peças
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, "3. DETALHAMENTO DA INTERVENCAO:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, f"Servico Realizado: {reg['Servico Realizado']}")
    pdf.multi_cell(0, 5, f"Pecas Substituidas: {reg['Pecas Substituidas']}")
    pdf.multi_cell(0, 5, f"Pendencias: {reg['Pendencias']}")
    pdf.multi_cell(0, 5, f"Pecas a Providenciar: {reg['Pecas a Providenciar']}")
    
    return bytes(pdf.output())

# ==============================================================================
# ⚙️ CORPO PRINCIPAL DO APP
# ==============================================================================
c_logo, c_title = st.columns([1, 3])
with c_logo:
    st.image(LOGO_URL, use_container_width=True)
with c_title:
    st.title("Vogon Group — Doctoring Specialist")
    st.caption("Sistema de Diagnóstico, Validação de Tolerâncias e Gestão Integrada")

st.divider()

# PARAMETRIZAÇÃO GERAL
st.sidebar.header("1. Identificação Geral")
cliente = st.sidebar.text_input("Nome do Cliente / Usina", value="Klabin")
maquina = st.sidebar.text_input("Identificação da Máquina", value="MP-01")
data_hoje = st.sidebar.date_input("Data da Intervenção", datetime.today())
tecnico = st.sidebar.text_input("Técnico Responsável", value=usr['nome'])

st.sidebar.divider()
st.sidebar.header("2. Posição da Máquina")
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

posicao_detalhada = st.sidebar.text_input("Posição Exata da Intervenção", value="Cilindro Secador 78")

def obter_regras_engenharia(grupo):
    if "Formadora" in grupo:
        return {"ang_min": 20, "ang_max": 25, "press_max": 200, "ref_ang": "20° a 25°", "ref_press": "100 a 200 N/m", "mat": "Sintética (UHMW / Epoxy)"}
    elif "Prensar" in grupo:
        return {"ang_min": 23, "ang_max": 32, "press_max": 350, "ref_ang": "23° a 32°", "ref_press": "200 a 350 N/m", "mat": "Bronze / Inox / Cerâmica"}
    elif "Secador" in grupo:
        return {"ang_min": 25, "ang_max": 32, "press_max": 250, "ref_ang": "25° a 32°", "ref_press": "150 a 250 N/m", "mat": "Aço Carbono / Fibra de Carbono"}
    elif "Yankee" in grupo:
        return {"ang_min": 16, "ang_max": 22, "press_max": 450, "ref_ang": "16° a 22°", "ref_press": "250 a 450 N/m", "mat": "Carbeto de Tungstênio / Cerâmica"}
    else:
        return {"ang_min": 25, "ang_max": 32, "press_max": 300, "ref_ang": "25° a 32°", "ref_press": "200 a 300 N/m", "mat": "Aço Inox / Cerâmica"}

regras = obter_regras_engenharia(grupo_posicao)

st.subheader(f"📍 Posição Selecionada: {posicao_detalhada}")
col_a, col_b, col_c = st.columns(3)
col_a.metric("Ângulo Tolerado (Max)", regras["ref_ang"])
col_b.metric("Pressão Limite Máxima", regras["ref_press"])
col_c.metric("Material Indicado", regras["mat"])

st.divider()

# AFERIÇÃO E VALIDAÇÃO DE PARÂMETROS
st.subheader("⚙️ Aferição de Ângulo e Pressão Ajustados")
col_input1, col_input2 = st.columns(2)

with col_input1:
    angulo_ajustado = st.number_input("Ângulo Real Ajustado na Viga (°)", value=float(regras["ang_min"]), step=0.5)
with col_input2:
    pressao_ajustada = st.number_input("Pressão Real Aplicada (N/m)", value=200.0, step=10.0)

fora_do_range_angulo = (angulo_ajustado < regras["ang_min"]) or (angulo_ajustado > regras["ang_max"])
fora_do_range_pressao = pressao_ajustada > regras["press_max"]
necessita_aprovacao = fora_do_range_angulo or fora_do_range_pressao

aprovador_nome = ""
if necessita_aprovacao:
    st.markdown(f"""
    <div class="alert-box">
        <h4 style="color: #C62828; margin-top:0px;">⚠️ ATENÇÃO: PARÂMETROS FORA DA TABELA DE ENGENHARIA!</h4>
        <p>O ângulo ({angulo_ajustado}°) ou pressão ({pressao_ajustada} N/m) excedem os limites da seção.</p>
        <p><b>A gravação exige a APROVAÇÃO do Gestor Vogon ou do Cliente responsável.</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    if usr['perfil'] in ['gestor', 'gestor_master']:
        aprovador_nome = f"{usr['nome']} ({usr['cargo']}) - Auto-aprovado via Login"
        st.success(f"✅ **Aprovação Automática:** Logado como **{aprovador_nome}**")
    else:
        aprovador_nome = st.text_input("👤 Nome e Cargo do Aprovador Responsável:")
else:
    st.success("✅ **Parâmetros Operacionais Válidos:** Dentro da faixa de tolerância autorizada.")

st.divider()

# ESPECIFICAÇÃO DE LÂMINAS
st.subheader("🔪 Especificação Técnica da Lâmina Instalada")
c_lam1, c_lam2 = st.columns(2)

with c_lam1:
    lamina_nome = st.text_input("Modelo / Código da Lâmina", value="Vogon Inox-Precision")
    lamina_material = st.selectbox("Material da Lâmina", ["Aço Inox 304/316L", "Aço Carbono Temperado", "Bronze Fosforoso", "Sintética / UHMW", "Fibra de Vidro", "Fibra de Carbono", "Carbeto de Tungstênio / Cerâmica", "Outro"])

with c_lam2:
    tipo_rebitagem = st.selectbox("Tipo de Rebitagem", ["DST", "KF", "DSTF", "KF Frontal", "A1", "Conformatic", "Sem Rebites", "Outros"])
    rebitagem_detalhe = st.text_input("Especifique a Rebitagem:", value="Padrão Especial Vogon") if tipo_rebitagem == "Outros" else tipo_rebitagem

st.markdown("##### 📐 Dimensões Geométricas (mm)")
c_dim1, c_dim2, c_dim3 = st.columns(3)
with c_dim1:
    lam_largura = st.number_input("Largura (mm)", value=76.2, step=1.0)
with c_dim2:
    lam_espessura = st.number_input("Espessura (mm)", value=1.20, step=0.05, format="%.2f")
with c_dim3:
    lam_comprimento = st.number_input("Comprimento (mm)", value=4500.0, step=10.0)

st.divider()

# REGISTRO FOTOGRÁFICO
st.subheader("📸 Fotos do Ajuste de Ângulos (LA / LC)")
col1, col2 = st.columns(2)
with col1:
    img_antes_la = st.file_uploader("Foto ANTES — Lado Acionamento (LA)", type=["jpg", "jpeg", "png"], key="la_a")
    img_depois_la = st.file_uploader("Foto DEPOIS — Lado Acionamento (LA)", type=["jpg", "jpeg", "png"], key="la_d")
with col2:
    img_antes_lc = st.file_uploader("Foto ANTES — Lado Comando (LC)", type=["jpg", "jpeg", "png"], key="lc_a")
    img_depois_lc = st.file_uploader("Foto DEPOIS — Lado Comando (LC)", type=["jpg", "jpeg", "png"], key="lc_d")

st.divider()

# DETALHES DO SERVIÇO
st.subheader("📝 Detalhes do Serviço nesta Posição")
c_f1, c_f2 = st.columns(2)
with c_f1:
    servico_feito = st.text_area("Serviço Realizado:", value="Ajuste do ângulo de ataque, verificação de pressão e troca de lâmina gasta.")
    pecas_substituidas = st.text_area("Peças Substituídas:", value=f"1x Lâmina {lamina_nome} ({lam_largura}x{lam_espessura}x{lam_comprimento} mm) Rebitagem {rebitagem_detalhe}.")
with c_f2:
    falta_fazer = st.text_area("Pendências / Falta Fazer:", value="Monitorar limpeza do tubo na próxima parada.")
    pecas_providenciar = st.text_area("Peças a Providenciar:", value="1x Kit de vedação de suporte.")

# SALVAR E DISPARAR NO WHATSAPP
st.divider()
bloquear_botao = necessita_aprovacao and (len(aprovador_nome.strip()) == 0)

if bloquear_botao:
    st.warning("🔒 **Ação Bloqueada:** Informe o **Aprovador Responsável** para gravar o parâmetro fora da tabela.")

if st.button("➕ Salvar Registro desta Posição na Planilha do Dia", disabled=bloquear_botao):
    status_aprovacao_txt = f"APROVADO POR: {aprovador_nome}" if necessita_aprovacao else "DENTRO DO PADRÃO ENGENHARIA"
    
    registro = {
        "Data": data_hoje.strftime("%d/%m/%Y"),
        "Cliente": cliente,
        "Maquina": maquina,
        "Tecnico Logado": usr['nome'],
        "Tipo Papel": tipo_papel,
        "Seção": grupo_posicao,
        "Posição Exata (Raspador)": posicao_detalhada,
        "Angulo Real (°)": angulo_ajustado,
        "Pressao Real (N/m)": pressao_ajustada,
        "Status Tolerancia": "FORA DO PADRÃO (APROVADO)" if necessita_aprovacao else "PADRÃO OK",
        "Aprovador Responsavel": status_aprovacao_txt,
        "Lamina Instalada": lamina_nome,
        "Material Lamina": lamina_material,
        "Dimensao Total (LxExC mm)": f"{lam_largura} x {lam_espessura} x {lam_comprimento}",
        "Tipo Rebitagem": rebitagem_detalhe,
        "Serviço Realizado": servico_feito,
        "Pecas Substituidas": pecas_substituidas,
        "Pendencias": falta_fazer,
        "Pecas a Providenciar": pecas_providenciar
    }
    st.session_state['historico_intervencao'].append(registro)
    st.success(f"✅ Intervenção na posição **'{posicao_detalhada}'** gravada no histórico do dia!")

    # MENSAGEM AUTOMÁTICA PARA WHATSAPP
    texto_wsp = f"""*VOGON GROUP - RELATÓRIO DE INTERVENÇÃO*
*Cliente:* {cliente} | *Máquina:* {maquina}
*Data:* {data_hoje.strftime("%d/%m/%Y")} | *Técnico:* {usr['nome']}
*Posição:* {posicao_detalhada}

*Ângulo Ajustado:* {angulo_ajustado}°
*Pressão Aplicada:* {pressao_ajustada} N/m
*Status:* {status_aprovacao_txt}

*Lâmina:* {lamina_nome} ({lam_largura}x{lam_espessura}x{lam_comprimento} mm) - Rebitagem {rebitagem_detalhe}
*Serviço:* {servico_feito}
*Peças Substituídas:* {pecas_substituidas}
*Pendências:* {falta_fazer}

_Gerado via Vogon Doctoring Specialist App_"""

    wsp_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(texto_wsp)}"
    
    st.markdown(f"""
        <a href="{wsp_url}" target="_blank">
            <button style="background-color: #25D366; color: white; padding: 10px 20px; border: none; border-radius: 5px; font-weight: bold; cursor: pointer;">
                📲 Enviar Resumo do Serviço via WhatsApp
            </button>
        </a>
    """, unsafe_allow_html=True)

# ==============================================================================
# 📂 CENTRAL DE GESTÃO & BOTÕES DE AÇÃO DOS GESTORES
# ==============================================================================
if len(st.session_state['historico_intervencao']) > 0:
    st.divider()
    
    # PAINEL EXCLUSIVO PARA GESTORES
    if usr['perfil'] in ['gestor', 'gestor_master']:
        st.markdown("""
        <div class="manager-box">
            <h3 style="color: #0E2F56; margin-top: 0px;">📂 Painel de Ação da Gestão Vogon</h3>
            <p style="font-size: 13px; color: #333;">Como Gestor, você tem acesso imediato para exportar os documentos completos (PDF e Excel) acumulados no dia.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("📊 Histórico de Intervenções Acumuladas Hoje")
    df_historico = pd.DataFrame(st.session_state['historico_intervencao'])
    
    colunas_visiveis = ["Data", "Cliente", "Maquina", "Posição Exata (Raspador)", "Angulo Real (°)", "Status Tolerancia", "Lamina Instalada"]
    st.dataframe(df_historico[colunas_visiveis], use_container_width=True)

    data_str = data_hoje.strftime("%Y-%m-%d")
    nome_base = f"{cliente.replace(' ', '_')}_{maquina.replace(' ', '_')}_{data_str}"

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        # GERAR PLANILHA EXCEL
        output_excel = io.BytesIO()
        with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
            df_historico.to_excel(writer, index=False, sheet_name='Intervençoes_Vogon')
        excel_bytes = output_excel.getvalue()

        st.download_button(
            label=f"📊 Baixar Planilha Excel ({nome_base}.xlsx)",
            data=excel_bytes,
            file_name=f"{nome_base}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with col_btn2:
        # GERAR PDF TIMBRADO DA ÚLTIMA INTERVENÇÃO
        ultimo_registro = st.session_state['historico_intervencao'][-1]
        pdf_bytes = gerar_pdf_timbrado(ultimo_registro)

        st.download_button(
            label=f"📄 Baixar Relatório PDF Timbrado ({nome_base}.pdf)",
            data=pdf_bytes,
            file_name=f"{nome_base}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
