import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

try:
    from zoneinfo import ZoneInfo
    _agora = datetime.now(ZoneInfo("America/Sao_Paulo"))
except Exception:
    _agora = datetime.now()

st.set_page_config(
    page_title="Controle de Medições | Augusto Engenharia",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== DESIGN ====================
# Paleta: azul-petróleo (estrutura), âmbar (sinalização de obra), concreto (fundo)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

    :root {
        --ink: #0F2A3D;
        --ink-soft: #4A5F70;
        --amber: #E8A317;
        --concrete: #EEF1F4;
        --line: #D5DCE3;
        --ok: #1F8A5B;
        --warn: #D98A0B;
        --bad: #C8453B;
    }

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .stApp { background-color: var(--concrete); }
    .block-container { padding-top: 0 !important; padding-bottom: 2.5rem; max-width: 1400px; }
    #MainMenu, footer, header {visibility: hidden;}

    /* Faixa de cabeçalho */
    .topbar {
        background: var(--ink);
        margin: 0 -4rem 1.6rem -4rem;
        padding: 1.5rem 4rem 1.3rem 4rem;
        border-bottom: 4px solid var(--amber);
        display: flex; justify-content: space-between; align-items: flex-end;
        flex-wrap: wrap; gap: 0.6rem;
    }
    .brand { color: #AFC3D3; font-size: 0.85rem; font-weight: 500; margin-bottom: 0.2rem; }
    .main-title { color: #FFFFFF; font-size: 1.7rem; font-weight: 700; margin: 0; letter-spacing: -0.3px; }
    .stamp { color: #AFC3D3; font-size: 0.82rem; text-align: right; }
    .stamp b { color: #FFFFFF; font-weight: 600; }

    /* Títulos de seção */
    .section-title {
        font-size: 1.05rem; font-weight: 600; color: var(--ink);
        margin: 0.4rem 0 0.7rem 0; padding-left: 0.6rem;
        border-left: 4px solid var(--amber);
    }

    /* Painel de filtros */
    div[data-testid="stHorizontalBlock"]:has(.filtro-marca) { align-items: end; }

    /* KPIs */
    .kpi-card {
        background: #FFFFFF; border: 1px solid var(--line); border-radius: 6px;
        padding: 1.05rem 1.25rem; min-height: 112px; height: 100%;
        display: flex; flex-direction: column; justify-content: center;
        border-left: 5px solid var(--ink);
    }
    .kpi-card.destaque { background: var(--ink); border-color: var(--ink); border-left-color: var(--amber); }
    .kpi-card.destaque .kpi-label, .kpi-card.destaque .kpi-sub { color: #AFC3D3; }
    .kpi-card.destaque .kpi-value { color: #FFFFFF; }
    .kpi-card.green { border-left-color: var(--ok); }
    .kpi-card.amber { border-left-color: var(--amber); }
    .kpi-card.slate { border-left-color: #6B8499; }

    .kpi-label { font-size: 0.82rem; color: var(--ink-soft); font-weight: 500; margin-bottom: 0.3rem; }
    .kpi-value {
        font-size: 1.5rem; font-weight: 700; color: var(--ink); margin: 0;
        line-height: 1.2; letter-spacing: -0.3px; font-variant-numeric: tabular-nums;
    }
    .kpi-sub { font-size: 0.78rem; color: var(--ink-soft); margin-top: 0.3rem; }

    /* Gráficos em painéis */
    .chart-title {
        font-size: 1rem; font-weight: 600; color: var(--ink);
        margin: 0 0 0.4rem 0;
    }
    div[data-testid="stPlotlyChart"] {
        background: #FFFFFF; border: 1px solid var(--line); border-radius: 6px; padding: 0.4rem;
    }

    /* Tabela */
    .stDataFrame { border: 1px solid var(--line); border-radius: 6px; overflow: hidden; background: #FFFFFF; }

    /* Filtros */
    label, .stSelectbox label, .stMultiSelect label { color: var(--ink) !important; font-weight: 500 !important; }

    hr { border-color: var(--line); margin: 1.2rem 0; }

    @media (max-width: 768px) {
        .topbar { margin: 0 -1rem 1.2rem -1rem; padding: 1.1rem 1rem; }
        .main-title { font-size: 1.3rem; }
        .stamp { text-align: left; }
        .kpi-value { font-size: 1.25rem; }
        .block-container { padding-left: 1rem; padding-right: 1rem; }
    }
</style>
""", unsafe_allow_html=True)

# ==================== DADOS (INALTERADOS) ====================
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

# ==================== CABEÇALHO ====================
st.markdown(f"""
<div class="topbar">
    <div>
        <div class="brand">Augusto Engenharia</div>
        <p class="main-title">Controle de Medições e Saldos</p>
    </div>
    <div class="stamp">Emitido em <b>{_agora.strftime("%d/%m/%Y")}</b> às <b>{_agora.strftime("%H:%M")}</b></div>
</div>
""", unsafe_allow_html=True)

# ==================== FILTROS ====================
st.markdown('<div class="section-title">Filtros</div>', unsafe_allow_html=True)
f1, f2, f3 = st.columns([1.2, 2.2, 1.2])

with f1:
    status_opcoes = ["Todos"] + sorted(df["Status"].unique().tolist())
    filtro_status = st.selectbox("Status da obra", status_opcoes)

with f2:
    filtro_obra = st.multiselect(
        "Selecionar obras",
        options=df["Nome da Obra"].tolist(),
        default=None,
        placeholder="Todas as obras"
    )

with f3:
    st.markdown("<div style='height: 1.9rem'></div>", unsafe_allow_html=True)
    mostrar_apenas_ativos = st.checkbox("Somente com contrato", value=True)

st.markdown("---")

# ==================== APLICAR FILTROS ====================
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

# ==================== INDICADORES ====================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi-card destaque">
        <div class="kpi-label">Saldo a receber</div>
        <p class="kpi-value">{brl(total_saldo)}</p>
        <div class="kpi-sub">Valor em aberto</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card green">
        <div class="kpi-label">Total medido</div>
        <p class="kpi-value">{brl(total_medido)}</p>
        <div class="kpi-sub">{perc_geral*100:.1f}% dos contratos</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card amber">
        <div class="kpi-label">Total de contratos</div>
        <p class="kpi-value">{brl(total_contrato)}</p>
        <div class="kpi-sub">{qtd_obras} obras</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card slate">
        <div class="kpi-label">% médio medido</div>
        <p class="kpi-value">{perc_geral*100:.1f}%</p>
        <div class="kpi-sub">Progresso geral</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 1.4rem'></div>", unsafe_allow_html=True)

# ==================== GRÁFICOS ====================
df_saldo = df_f[df_f["Saldo a Receber"] > 0].sort_values("Saldo a Receber", ascending=True)
df_perc  = df_f[df_f["Valor Contrato"] > 0].sort_values("% Medido", ascending=True)

n_barras = max(len(df_saldo), len(df_perc), 1)
altura_grafico = max(280, min(38 * n_barras + 80, 600))

FONTE = dict(family="IBM Plex Sans", size=12, color="#0F2A3D")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<p class="chart-title">Saldo a receber por obra</p>', unsafe_allow_html=True)
    if not df_saldo.empty:
        fig = px.bar(
            df_saldo,
            x="Saldo a Receber",
            y="Nome da Obra",
            orientation="h",
            text="Saldo a Receber",
            color="Saldo a Receber",
            color_continuous_scale=["#9DB4C6", "#0F2A3D"],
        )
        fig.update_traces(
            texttemplate="R$ %{x:,.0f}",
            textposition="outside",
            marker_line_width=0,
            textfont=dict(size=11, color="#0F2A3D"),
            cliponaxis=False,
        )
        fig.update_layout(
            height=altura_grafico,
            margin=dict(l=8, r=80, t=8, b=8),
            xaxis_title="",
            yaxis_title="",
            coloraxis_showscale=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=FONTE,
            xaxis=dict(showgrid=True, gridcolor="#E6EBF0", tickprefix="R$ ", automargin=True),
            yaxis=dict(automargin=True),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Nenhuma obra com saldo no filtro atual.")

with col2:
    st.markdown('<p class="chart-title">% medido por obra</p>', unsafe_allow_html=True)
    if not df_perc.empty:
        cores = ["#C8453B" if x < 0.30 else "#E8A317" if x < 0.70 else "#1F8A5B" for x in df_perc["% Medido"]]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=df_perc["% Medido"] * 100,
            y=df_perc["Nome da Obra"],
            orientation="h",
            marker_color=cores,
            text=[f"{v*100:.1f}%" for v in df_perc["% Medido"]],
            textposition="outside",
            textfont=dict(size=11, color="#0F2A3D"),
            cliponaxis=False,
        ))
        fig2.update_layout(
            height=altura_grafico,
            margin=dict(l=8, r=55, t=8, b=8),
            xaxis=dict(title="", range=[0, 120], ticksuffix="%", showgrid=True, gridcolor="#E6EBF0", automargin=True),
            yaxis=dict(title="", automargin=True),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=FONTE,
            showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.caption("Faixas de cor: abaixo de 30% • de 30% a 70% • acima de 70%")
    else:
        st.info("Sem dados de percentual.")

# ==================== TABELA ====================
st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Detalhamento por obra</div>', unsafe_allow_html=True)

df_show = df_f.copy()
df_show["Valor Contrato"]  = df_show["Valor Contrato"].apply(brl)
df_show["Total Medido"]    = df_show["Total Medido"].apply(brl)
df_show["Saldo a Receber"] = df_show["Saldo a Receber"].apply(brl)
df_show["% Medido"]        = df_show["% Medido"] * 100  # exibido como barra de progresso

df_show = df_show[["Nº", "Nome da Obra", "Valor Contrato", "Total Medido", "Saldo a Receber", "% Medido", "Status"]]

def cor_status(v):
    if v == "Ativo":
        return "background-color: #DDF1E8; color: #14633F; font-weight: 600;"
    return "background-color: #FBEBC8; color: #7A5200; font-weight: 600;"

estilo = df_show.style
_aplicar = getattr(estilo, "map", None) or estilo.applymap
estilo = _aplicar(cor_status, subset=["Status"])
estilo = estilo.set_properties(
    subset=["Valor Contrato", "Total Medido", "Saldo a Receber"],
    **{"text-align": "right"}
)

altura_tabela = min(52 * (len(df_show) + 1), 500)

st.dataframe(
    estilo,
    use_container_width=True,
    hide_index=True,
    height=altura_tabela,
    column_config={
        "Nº": st.column_config.NumberColumn("Nº", width="small"),
        "Nome da Obra": st.column_config.TextColumn("Obra", width="medium"),
        "% Medido": st.column_config.ProgressColumn(
            "% Medido", format="%.1f%%", min_value=0, max_value=100
        ),
    },
)

st.markdown("---")
st.caption("Augusto Engenharia • Controle de Medições e Saldos • Uso interno")
