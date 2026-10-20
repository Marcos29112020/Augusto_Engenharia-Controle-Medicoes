import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Controle de Medições | Augusto Engenharia",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== DESIGN CORPORATIVO LIMPO ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: #F8FAFC;
    }

    .block-container {
        padding-top: 1.6rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Título */
    .main-title {
        font-size: 1.65rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.1rem;
        letter-spacing: -0.4px;
    }
    .sub-title {
        color: #64748B;
        font-size: 0.88rem;
        margin-bottom: 1.4rem;
        font-weight: 500;
    }

    /* KPI Cards - brancos com borda sutil */
    .kpi-card {
        background: #FFFFFF;
        padding: 1.25rem 1.35rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
        border: 1px solid #E2E8F0;
        height: 100%;
        min-height: 105px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .kpi-label {
        font-size: 0.7rem;
        color: #64748B;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }
    .kpi-value {
        font-size: 1.35rem;
        font-weight: 700;
        color: #0F172A;
        margin: 0;
        letter-spacing: -0.3px;
        line-height: 1.25;
    }
    .kpi-sub {
        font-size: 0.72rem;
        color: #94A3B8;
        margin-top: 0.3rem;
        font-weight: 500;
    }
    .kpi-value.blue   { color: #1E40AF; }
    .kpi-value.green  { color: #047857; }
    .kpi-value.orange { color: #C2410C; }
    .kpi-value.teal   { color: #0F766E; }

    /* Sidebar clara e limpa */
    section[data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stCheckbox label {
        font-weight: 600;
        color: #334155 !important;
        font-size: 0.85rem;
    }

    h3 {
        color: #0F172A !important;
        font-weight: 650 !important;
        font-size: 1.05rem !important;
        margin-bottom: 0.6rem !important;
    }

    .stDataFrame {
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        overflow: hidden;
    }

    /* Botão de reabrir sidebar mais visível */
    button[kind="header"] {
        background-color: #1E40AF !important;
        color: white !important;
        border-radius: 6px !important;
    }

    #MainMenu, footer, header {visibility: hidden;}

    /* ===== SETA DO FILTRO BEM VISÍVEL ===== */
    [data-testid="collapsedControl"] {
        background-color: #1E40AF !important;
        color: white !important;
        border-radius: 0 10px 10px 0 !important;
        padding: 12px 10px !important;
        box-shadow: 2px 2px 10px rgba(30, 64, 175, 0.35) !important;
        border: none !important;
    }
    [data-testid="collapsedControl"]:hover {
        background-color: #1D4ED8 !important;
    }
    [data-testid="collapsedControl"] svg {
        fill: white !important;
        width: 20px !important;
        height: 20px !important;
    }

    @media (max-width: 768px) {
        .kpi-value { font-size: 1.15rem; }
        .main-title { font-size: 1.3rem; }
        .block-container { padding-left: 0.85rem; padding-right: 0.85rem; }
    }
</style>
""", unsafe_allow_html=True)

# ==================== DADOS ====================
@st.cache_data(ttl=300)
def carregar_dados():
    data = {
        "Nº": list(range(1, 16)),
        "Nome da Obra": [
            "Vibra Marajoara", "Vibra Marechal Tito", "Vibra Adolfo Pinheiros",
            "Vibra Sapopemba Inst.", "Vibra Sapopemba Kits", "Vibra Sapopemba Estr.",
            "MRV Ritmos da Barra", "MRV City",
            "Vibra Campo Limpo Estr.", "Vibra Campo Limpo Inst.",
            "Look Ibirapuera Sinco", "Canopus TODAY Clementino", "Vibra Carrão",
            "Vibra Mooca", "Vibra Sabará"
        ],
        "Valor Contrato": [
            2066533.17, 4169795.00, 3740444.20, 1900000.00, 199500.00,
            3871007.00, 0, 0,
            5234888.52, 2940200.00,
            4149157.80, 0, 2568100.00, 4237920.00, 0
        ],
        "Total Medido": [
            1778085.40, 2276079.74, 3198871.30, 673058.03, 104595.00,
            2646656.95, 0, 0,
            29673.75, 0,
            451807.84, 0, 86042.63, 0, 0
        ],
        "Saldo a Receber": [
            288447.77, 1893715.26, 541572.90, 1226941.97, 94905.00,
            1224350.05, 0, 0,
            5205214.77, 2940200.00,
            3697349.96, 0, 2482057.37, 4237920.00, 0
        ],
        "% Medido": [
            0.8604, 0.5458, 0.8552, 0.3542, 0.5243,
            0.6837, 0, 0,
            0.0057, 0.0,
            0.1089, 0, 0.0335, 0.0, 0
        ],
        "Status": [
            "Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo",
            "Aguardando contrato", "Aguardando contrato",
            "Ativo", "Ativo",
            "Ativo", "Aguardando contrato", "Ativo",
            "Ativo", "Aguardando contrato"
        ]
    }
    return pd.DataFrame(data)

df = carregar_dados()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### Filtros")
    st.caption("Use os filtros abaixo para analisar as obras")
    
    status_opcoes = ["Todos"] + sorted(df["Status"].unique().tolist())
    filtro_status = st.selectbox("Status da Obra", status_opcoes)
    
    filtro_obra = st.multiselect(
        "Selecionar Obras",
        options=df["Nome da Obra"].tolist(),
        default=None,
        placeholder="Todas as obras"
    )
    
    st.markdown("---")
    mostrar_apenas_ativos = st.checkbox("Somente obras com contrato", value=True)
    
    st.markdown("---")
    st.markdown("**Augusto Engenharia**")
    st.caption(f"Atualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    st.caption("Uso interno")

# ==================== FILTROS ====================
df_f = df.copy()
if filtro_status != "Todos":
    df_f = df_f[df_f["Status"] == filtro_status]
if filtro_obra:
    df_f = df_f[df_f["Nome da Obra"].isin(filtro_obra)]
if mostrar_apenas_ativos:
    df_f = df_f[df_f["Valor Contrato"] > 0]

total_contrato = df_f["Valor Contrato"].sum()
total_medido   = df_f["Total Medido"].sum()
total_saldo    = df_f["Saldo a Receber"].sum()
perc_geral     = (total_medido / total_contrato) if total_contrato > 0 else 0
qtd_obras      = len(df_f)
qtd_ativas     = len(df_f[df_f["Status"] == "Ativo"])

def brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ==================== CABEÇALHO ====================
st.markdown('<p class="main-title">Controle de Medições e Saldos</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">{qtd_obras} obras • {qtd_ativas} ativas • Augusto Engenharia</p>', unsafe_allow_html=True)

# ==================== CARDS ====================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Saldo a Receber</div>
        <p class="kpi-value blue">{brl(total_saldo)}</p>
        <div class="kpi-sub">Valor em aberto</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Medido</div>
        <p class="kpi-value green">{brl(total_medido)}</p>
        <div class="kpi-sub">{perc_geral*100:.1f}% dos contratos</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Contratos</div>
        <p class="kpi-value orange">{brl(total_contrato)}</p>
        <div class="kpi-sub">{qtd_obras} obras</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">% Médio Medido</div>
        <p class="kpi-value teal">{perc_geral*100:.1f}%</p>
        <div class="kpi-sub">Progresso geral</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 1.1rem'></div>", unsafe_allow_html=True)

# ==================== GRÁFICOS ====================
df_saldo = df_f[df_f["Saldo a Receber"] > 0].sort_values("Saldo a Receber", ascending=True)
df_perc  = df_f[df_f["Valor Contrato"] > 0].sort_values("% Medido", ascending=True)

n_barras = max(len(df_saldo), len(df_perc), 1)
altura_grafico = max(280, min(38 * n_barras + 80, 600))

col1, col2 = st.columns(2)

with col1:
    st.subheader("Saldo a Receber por Obra")
    if not df_saldo.empty:
        fig = px.bar(
            df_saldo,
            x="Saldo a Receber",
            y="Nome da Obra",
            orientation="h",
            text="Saldo a Receber",
            color="Saldo a Receber",
            color_continuous_scale=["#BFDBFE", "#1E40AF"],
        )
        fig.update_traces(
            texttemplate="R$ %{x:,.0f}",
            textposition="outside",
            marker_line_width=0,
            textfont=dict(size=11, color="#334155"),
            cliponaxis=False,
        )
        fig.update_layout(
            height=altura_grafico,
            margin=dict(l=8, r=70, t=8, b=8),
            xaxis_title="",
            yaxis_title="",
            coloraxis_showscale=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=12, color="#334155"),
            xaxis=dict(showgrid=True, gridcolor="#F1F5F9", tickprefix="R$ ", automargin=True),
            yaxis=dict(automargin=True),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Nenhuma obra com saldo no filtro atual.")

with col2:
    st.subheader("% Medido por Obra")
    if not df_perc.empty:
        cores = ["#EF4444" if x < 0.30 else "#F59E0B" if x < 0.70 else "#10B981" for x in df_perc["% Medido"]]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=df_perc["% Medido"] * 100,
            y=df_perc["Nome da Obra"],
            orientation="h",
            marker_color=cores,
            text=[f"{v*100:.1f}%" for v in df_perc["% Medido"]],
            textposition="outside",
            textfont=dict(size=11, color="#334155"),
            cliponaxis=False,
        ))
        fig2.update_layout(
            height=altura_grafico,
            margin=dict(l=8, r=55, t=8, b=8),
            xaxis=dict(title="", range=[0, 120], ticksuffix="%", showgrid=True, gridcolor="#F1F5F9", automargin=True),
            yaxis=dict(title="", automargin=True),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=12, color="#334155"),
            showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Sem dados de percentual.")

# ==================== TABELA ====================
st.subheader("Detalhamento por Obra")

df_show = df_f.copy()
df_show["Valor Contrato"]  = df_show["Valor Contrato"].apply(brl)
df_show["Total Medido"]    = df_show["Total Medido"].apply(brl)
df_show["Saldo a Receber"] = df_show["Saldo a Receber"].apply(brl)
df_show["% Medido"]        = df_show["% Medido"].apply(lambda x: f"{x*100:.1f}%")

altura_tabela = min(52 * (len(df_show) + 1), 500)

st.dataframe(
    df_show[["Nº", "Nome da Obra", "Valor Contrato", "Total Medido", "Saldo a Receber", "% Medido", "Status"]],
    use_container_width=True,
    hide_index=True,
    height=altura_tabela,
)

st.markdown("---")
st.caption("Augusto Engenharia • Controle de Medições e Saldos • Uso interno")
