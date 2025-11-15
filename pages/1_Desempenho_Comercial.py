"""
============================================================================
PROJETO INTEGRADOR - APOIO DECISÓRIO AOS NEGÓCIOS
Script da Seção 1.1 - Desempenho Comercial
Autor: Aline Morais
Data: 13/11/2025
Descrição: Script Python para utilizar o streamlit
============================================================================
"""

import pickle
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Carregar os DataFrames
with open('dataframes/dataframes.pkl', 'rb') as f:
    dfs = pickle.load(f)

# Titulo da página
st.title("🚗 1.1 Vendas e Desempenho Comercial")

# Usar as métricas principais em colunas como card
col1, col2, col3 = st.columns(3)
#####################
# Metrics principais
#####################

# Total de Vendas (valor direto)

col1.metric(
    "📋 Total de Vendas",
    f"{int(dfs['df_total']['Valor'][0]):,}".replace(",", ".")
)

# Receita Total

# Função para formatar números grandes
def formatar_numero(valor):
    if valor >= 1_000_000_000:
        return f"{valor/1_000_000_000:.1f} bi"
    elif valor >= 1_000_000:
        return f"{valor/1_000_000:.1f} mi"
    elif valor >= 1_000:
        return f"{valor/1_000:.1f} mil"
    else:
        return str(valor)

df_receita = dfs['df_receita_total']  # acessa o DataFrame

valor = df_receita.loc[df_receita['Métrica'] == 'Receita Total', 'Valor'].values[0]

valor_formatado = formatar_numero(valor)

col2.metric("📋 Receita Total", valor_formatado)

# Ticket Médio

col3.metric(
    "📋 Ticket Médio",
    f"${(df_receita.loc[df_receita['Métrica'] == 'Ticket Médio', 'Valor'].values[0]):,.2f}"
    .replace(",", "X").replace(".", ",").replace("X", ".")
)

# Modelos e marcas mais vendidos
st.subheader(" 📈 Modelos e marcas mais vendidos")

# Ordenar pelo maior valor
dfs['df_modelos_vendidos'] = dfs['df_modelos_vendidos'].sort_values(by="Receita Total", ascending=False)

# Função para formatar moeda
def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

df = dfs['df_modelos_vendidos'].copy()

# Formatar colunas desejadas
df['Receita Total'] = df['Receita Total'].apply(formatar_moeda)
df['Preço Médio'] = df['Preço Médio'].apply(formatar_moeda)

st.dataframe(df.head(10))

########################
# Tabela - Share por quantidade vendida
########################

st.subheader(" 📈 Share por quantidade vendida")

df_modelos = dfs['df_modelos_vendidos'] 

# Agrupa por marca e soma a quantidade
df_share_marca = (
    df_modelos.groupby('Marca', as_index=False)['Quantidade']
    .sum()
)

# Calcula o percentual de participação (numérico)
df_share_marca['Share_num'] = (
    df_share_marca['Quantidade'] / df_share_marca['Quantidade'].sum() * 100
)

# Ordena pelo maior percentual
df_share_marca = df_share_marca.sort_values(by='Share_num', ascending=False)

# Formata para exibir com 2 casas decimais e símbolo de porcentagem
df_share_marca['Share (%)'] = df_share_marca['Share_num'].apply(
    lambda x: f"{x:.2f}%"
)

# Remove a coluna numérica se não quiser exibir
df_share_marca = df_share_marca[['Marca', 'Quantidade', 'Share (%)']]

# Exibe no Streamlit
st.dataframe(df_share_marca)

######################
# Tabela - Share por receita total
#####################

st.subheader("📈 Share por receita total")

# Agrupa por marca e soma a receita
df_share_receita = (
    df_modelos.groupby('Marca', as_index=False)['Receita Total']
    .sum()
)

# Cálculo numérico do percentual
df_share_receita['Share_num'] = (
    df_share_receita['Receita Total'] / df_share_receita['Receita Total'].sum() * 100
)

# Ordenar pelo percentual numérico
df_share_receita = df_share_receita.sort_values(by='Share_num', ascending=False)

# ---- FORMATAÇÕES ----

# Formatar moeda (R$)
def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

df_share_receita['Receita Total'] = df_share_receita['Receita Total'].apply(formatar_moeda)

# Formatar percentual
df_share_receita['Share Receita (%)'] = df_share_receita['Share_num'].apply(
    lambda x: f"{x:.2f}%"
)

# Tabela final (sem a coluna numérica auxiliar)
df_share_receita = df_share_receita[['Marca', 'Receita Total', 'Share Receita (%)']]

# Exibir
st.dataframe(df_share_receita)

#####################
#  Gráfico de Barras - Receita por Marca
#####################

st.subheader("📊 Receita Total por Marca")

# Agrupar os dados por marca — SEM formatação
df_receita = (
    df_modelos.groupby('Marca', as_index=False)['Receita Total']
    .sum()
)

# Criar coluna numérica para o gráfico (garante que é float)
df_receita['Receita_num'] = df_receita['Receita Total'].astype(float)

# Criar coluna formatada apenas para exibição em tabela (não usada no gráfico)
def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

df_receita['Receita Total'] = df_receita['Receita_num'].apply(formatar_moeda)

# ---- GRÁFICO (usa Receita_num) ----
fig = px.bar(
    df_receita,
    x='Marca',
    y='Receita_num',
    text=df_receita['Receita_num'].apply(lambda x: f"R$ {x:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")),
)

fig.update_traces(textposition='outside')
fig.update_layout(
    yaxis_title="Receita Total (R$)",
    xaxis_title="Marca",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

#####################
#   Gráfico de Linhas - Taxa de Crescimento
#####################

st.markdown("#### 📊 Taxa de Crescimento")

df = dfs['df_vendas_mes'].copy()

fig = px.line(
    df,
    x='Mês',
    y='Receita',
    markers=True,
)

fig.update_layout(
    xaxis_title="Mês",
    yaxis_title="Receita",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

#####################
#   Gráfico de Pizza - Participação por Marca
#####################

# Paleta personalizada (10 cores)
cores = [
    "#3A7DFF",  # azul forte
    "#FF6FB1",  # rosa
    "#00A676",  # verde
    "#F4A259",  # laranja suave
    "#8D5B4C",  # marrom elegante
    "#6A4C93",  # roxo
    "#D4A017",  # dourado
    "#FF4F4F",  # vermelho claro
    "#0096C7",  # azul petróleo
    "#8ECae6"   # azul claro
]
st.markdown("#### 📊 Participação por Marca — Quantidade Vendida")
fig = px.pie(
    dfs["df_top_marcas"],
    names="Marca",
    values="Quantidade",
    hole=0.45,
    color="Marca",
    color_discrete_sequence=cores
)

fig.update_traces(
    textinfo="percent",
    pull=[0.03] * len(dfs["df_top_marcas"]),  # efeito de leve destaque
    hovertemplate="<b>%{label}</b><br>" +
                  "Quantidade: %{value}<br>" +
                  "Receita Total: R$ %{customdata}<extra></extra>",
    customdata=dfs["df_receita_total"]
)

fig.update_layout(
    showlegend=True,
    legend_title="Marca",
    template="plotly_white",
    margin=dict(t=60, b=20, l=20, r=20),
)

st.plotly_chart(fig, use_container_width=True)