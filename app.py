import streamlit as st
import pandas as pd
import plotly.express as px

# --- Config ---
st.set_page_config(page_title="Dashboard Car Sales", layout="wide")

# --- Leitura dos dados ---
df = pd.read_csv("data/car_data.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["year"] = df["Date"].dt.year
df["month"] = df["Date"].dt.to_period("M")
df["quarter"] = df["Date"].dt.to_period("Q")

# ==== SIDEBAR FILTERS ====
st.sidebar.header("Filtros")

year_filter = st.sidebar.multiselect(
    "Ano", options=df["year"].unique(), default=df["year"].unique()
)

quarter_filter = st.sidebar.multiselect(
    "Trimestre", options=df["quarter"].unique(), default=df["quarter"].unique()
)

df = df[df["year"].isin(year_filter)]
df = df[df["quarter"].isin(quarter_filter)]

# ==== KPIs ====
total_sales = df["Car_id"].count()
total_revenue = df["Price ($)"].sum()
avg_ticket = df["Price ($)"].mean()

# Crescimento mensal
sales_by_month = df.groupby("month")["Car_id"].count()
growth_monthly = sales_by_month.pct_change().fillna(0) * 100
last_growth_m = growth_monthly.iloc[-1]

# Crescimento trimestral
sales_by_quarter = df.groupby("quarter")["Car_id"].count()
growth_quarterly = sales_by_quarter.pct_change().fillna(0) * 100
last_growth_q = growth_quarterly.iloc[-1]

# ==== LAYOUT ====
st.title("🚘 Dashboard de Vendas de Carros")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Carros Vendidos", f"{total_sales:,}")
col2.metric("Receita Total", f"$ {total_revenue:,.2f}")
col3.metric("Ticket Médio", f"$ {avg_ticket:,.2f}")
col4.metric(
    "Cresc. Último Mês",
    f"{last_growth_m:,.2f}%",
    delta=f"{last_growth_m:,.2f}%"
)

st.divider()

# ==== Gráficos ====
colA, colB = st.columns(2)

with colA:
    st.subheader("📈 Vendas Mensais")
    fig_m = px.line(
        sales_by_month,
        x=sales_by_month.index.astype(str),
        y=sales_by_month.values,
        markers=True,
        labels={"x": "Mês", "y": "Vendas"}
    )
    fig_m.update_layout(margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_m, use_container_width=True)

with colB:
    st.subheader("📊 Crescimento Mensal (%)")
    fig_gm = px.bar(
        growth_monthly,
        x=growth_monthly.index.astype(str),
        y=growth_monthly.values,
        labels={"x": "Mês", "y": "% Crescimento"},
        text_auto=".2f"
    )
    fig_gm.update_layout(margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_gm, use_container_width=True)

st.divider()

colC, colD = st.columns(2)

with colC:
    st.subheader("📈 Vendas por Trimestre")
    fig_q = px.line(
        sales_by_quarter,
        x=sales_by_quarter.index.astype(str),
        y=sales_by_quarter.values,
        markers=True,
        labels={"x": "Trimestre", "y": "Vendas"}
    )
    st.plotly_chart(fig_q, use_container_width=True)

with colD:
    st.subheader("📊 Crescimento Trimestral (%)")
    fig_gq = px.bar(
        growth_quarterly,
        x=growth_quarterly.index.astype(str),
        y=growth_quarterly.values,
        text_auto=".2f",
        labels={"x": "Trimestre", "y": "% Crescimento"}
    )
    st.plotly_chart(fig_gq, use_container_width=True)

st.divider()

# ==== TABELA DETALHADA ====
st.subheader("📋 Dados Agregados por Mês")
summary = pd.DataFrame({
    "Vendas": sales_by_month,
    "Crescimento (%)": growth_monthly.round(2),
})
st.dataframe(summary, use_container_width=True)
