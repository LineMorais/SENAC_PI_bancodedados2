#!/usr/bin/env python3
"""
============================================================================
PROJETO INTEGRADOR - APOIO DECISÓRIO AOS NEGÓCIOS
Script de Geração de DataFrames para Streamlit
Autor: David Carvalho
Data: 10/11/2025
Descrição: Gera DataFrames estruturados para visualização no Streamlit
============================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime
import pickle

# Carregar dados do CSV
print("="*80)
print("GERAÇÃO DE DATAFRAMES PARA STREAMLIT")
print("="*80)

print("\n→ Carregando dados do CSV...")
df = pd.read_csv('car_sales.csv')

# Transformar data
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Quarter'] = df['Date'].dt.quarter
df['YearMonth'] = df['Date'].dt.to_period('M').astype(str)

print(f"✓ Dados carregados: {len(df)} registros")

# ============================================================================
# DATAFRAMES PARA VENDAS E DESEMPENHO COMERCIAL
# ============================================================================

print("\n→ Gerando DataFrames de Vendas e Desempenho...")

# 1. Volume total de vendas
df_total = pd.DataFrame({
    'Métrica': ['Total de Vendas'],
    'Valor': [len(df)]
})

# 2. Receita total e média
df_receita_total = pd.DataFrame({
    'Métrica': ['Receita Total', 'Ticket Médio'],
    'Valor': [df['Price ($)'].sum(), df['Price ($)'].mean()]
})

# 3. Taxa de crescimento mensal
df_vendas_mes = df.groupby('YearMonth').agg({
    'Car_id': 'count',
    'Price ($)': 'sum'
}).reset_index()
df_vendas_mes.columns = ['Mês', 'Quantidade', 'Receita']
df_vendas_mes['Crescimento (%)'] = df_vendas_mes['Receita'].pct_change() * 100

# 4. Modelos e marcas mais vendidos
df_modelos_vendidos = df.groupby(['Company', 'Model']).agg({
    'Car_id': 'count',
    'Price ($)': ['sum', 'mean']
}).reset_index()
df_modelos_vendidos.columns = ['Marca', 'Modelo', 'Quantidade', 'Receita Total', 'Preço Médio']
df_modelos_vendidos = df_modelos_vendidos.sort_values('Quantidade', ascending=False)

# 5. Vendas por trimestre (sazonalidade)
df_sazonalidade = df.groupby(['Year', 'Quarter']).agg({
    'Car_id': 'count',
    'Price ($)': 'sum'
}).reset_index()
df_sazonalidade.columns = ['Ano', 'Trimestre', 'Quantidade', 'Receita']

print("✓ DataFrames de vendas gerados")

# ============================================================================
# DATAFRAMES PARA PERFIL DO CLIENTE
# ============================================================================

print("\n→ Gerando DataFrames de Perfil do Cliente...")

# 6. Criar faixa de renda
def categorize_income(income):
    if income < 50000:
        return 'Baixa (< 50k)'
    elif income < 100000:
        return 'Média-Baixa (50k-100k)'
    elif income < 500000:
        return 'Média (100k-500k)'
    elif income < 1000000:
        return 'Média-Alta (500k-1M)'
    else:
        return 'Alta (> 1M)'

df['Faixa_Renda'] = df['Annual Income'].apply(categorize_income)

# 7. Distribuição por faixa de renda
df_agrupar_faixa_renda = df.groupby('Faixa_Renda').agg({
    'Car_id': 'count',
    'Price ($)': 'mean',
    'Annual Income': 'mean'
}).reset_index()
df_agrupar_faixa_renda.columns = ['Faixa de Renda', 'Quantidade', 'Preço Médio', 'Renda Média']
df_agrupar_faixa_renda['Percentual (%)'] = (df_agrupar_faixa_renda['Quantidade'] / len(df)) * 100

# 8. Percentual por gênero
df_genero = df.groupby('Gender').agg({
    'Car_id': 'count',
    'Price ($)': 'mean',
    'Annual Income': 'mean'
}).reset_index()
df_genero.columns = ['Gênero', 'Quantidade', 'Preço Médio', 'Renda Média']
df_genero['Percentual (%)'] = (df_genero['Quantidade'] / len(df)) * 100

# 9. Índice de esforço financeiro (preço / renda)
df['Esforco_Financeiro'] = df['Price ($)'] / df['Annual Income']
df_renda_x_modelo = df.groupby(['Faixa_Renda', 'Model']).agg({
    'Car_id': 'count',
    'Price ($)': 'mean',
    'Esforco_Financeiro': 'mean'
}).reset_index()
df_renda_x_modelo.columns = ['Faixa de Renda', 'Modelo', 'Quantidade', 'Preço Médio', 'Esforço Financeiro']
df_renda_x_modelo = df_renda_x_modelo.sort_values(['Faixa de Renda', 'Quantidade'], ascending=[True, False])

# 10. Preferências por faixa de renda e gênero
df_preferencias = df.groupby(['Faixa_Renda', 'Gender', 'Company']).agg({
    'Car_id': 'count',
    'Price ($)': 'mean'
}).reset_index()
df_preferencias.columns = ['Faixa de Renda', 'Gênero', 'Marca', 'Quantidade', 'Preço Médio']
df_preferencias = df_preferencias.sort_values(['Faixa de Renda', 'Quantidade'], ascending=[True, False])

print("✓ DataFrames de perfil do cliente gerados")

# ============================================================================
# DATAFRAMES PARA ANÁLISE REGIONAL
# ============================================================================

print("\n→ Gerando DataFrames de Análise Regional...")

# 11. Receita por região
df_receita_regiao = df.groupby('Dealer_Region').agg({
    'Car_id': 'count',
    'Price ($)': 'sum'
}).reset_index()
df_receita_regiao.columns = ['Região', 'Quantidade', 'Receita Total']
df_receita_regiao['Percentual (%)'] = (df_receita_regiao['Receita Total'] / df_receita_regiao['Receita Total'].sum()) * 100
df_receita_regiao = df_receita_regiao.sort_values('Receita Total', ascending=False)

# 12. Ticket médio por concessionária
df_ticket_medio_concessionaria = df.groupby(['Dealer_Name', 'Dealer_Region']).agg({
    'Car_id': 'count',
    'Price ($)': ['sum', 'mean']
}).reset_index()
df_ticket_medio_concessionaria.columns = ['Concessionária', 'Região', 'Quantidade', 'Receita Total', 'Ticket Médio']
df_ticket_medio_concessionaria = df_ticket_medio_concessionaria.sort_values('Ticket Médio', ascending=False)

# 13. Ranking de concessionárias
df_ranking = df.groupby(['Dealer_Name', 'Dealer_Region']).agg({
    'Car_id': 'count',
    'Price ($)': 'sum'
}).reset_index()
df_ranking.columns = ['Concessionária', 'Região', 'Quantidade', 'Receita Total']
df_ranking = df_ranking.sort_values('Quantidade', ascending=False)
df_ranking['Ranking'] = range(1, len(df_ranking) + 1)

# 14. Comparação entre regiões
df_comparacao_regioes = df.groupby('Dealer_Region').agg({
    'Dealer_Name': 'nunique',
    'Car_id': 'count',
    'Price ($)': ['sum', 'mean']
}).reset_index()
df_comparacao_regioes.columns = ['Região', 'Nº Concessionárias', 'Quantidade', 'Receita Total', 'Ticket Médio']
df_comparacao_regioes['Receita por Concessionária'] = df_comparacao_regioes['Receita Total'] / df_comparacao_regioes['Nº Concessionárias']

print("✓ DataFrames de análise regional gerados")

# ============================================================================
# DATAFRAMES ADICIONAIS PARA VISUALIZAÇÕES
# ============================================================================

print("\n→ Gerando DataFrames adicionais...")

# 15. Vendas por tipo de carroceria
df_body_style = df.groupby('Body Style').agg({
    'Car_id': 'count',
    'Price ($)': ['sum', 'mean']
}).reset_index()
df_body_style.columns = ['Tipo de Carroceria', 'Quantidade', 'Receita Total', 'Preço Médio']
df_body_style = df_body_style.sort_values('Quantidade', ascending=False)

# 16. Vendas por transmissão
df_transmission = df.groupby('Transmission').agg({
    'Car_id': 'count',
    'Price ($)': 'mean'
}).reset_index()
df_transmission.columns = ['Transmissão', 'Quantidade', 'Preço Médio']

# 17. Vendas por cor
df_color = df.groupby('Color').agg({
    'Car_id': 'count',
    'Price ($)': 'mean'
}).reset_index()
df_color.columns = ['Cor', 'Quantidade', 'Preço Médio']
df_color = df_color.sort_values('Quantidade', ascending=False)

# 18. Top 10 marcas
df_top_marcas = df.groupby('Company').agg({
    'Car_id': 'count',
    'Price ($)': ['sum', 'mean']
}).reset_index()
df_top_marcas.columns = ['Marca', 'Quantidade', 'Receita Total', 'Preço Médio']
df_top_marcas = df_top_marcas.sort_values('Quantidade', ascending=False).head(10)

# 19. Evolução temporal das vendas
df_evolucao = df.groupby('Date').agg({
    'Car_id': 'count',
    'Price ($)': 'sum'
}).reset_index()
df_evolucao.columns = ['Data', 'Quantidade', 'Receita']

# 20. Matriz de correlação entre variáveis numéricas
df_correlacao = df[['Annual Income', 'Price ($)', 'Esforco_Financeiro']].corr()

print("✓ DataFrames adicionais gerados")

# ============================================================================
# SALVAR DATAFRAMES
# ============================================================================

print("\n→ Salvando DataFrames...")

# Criar dicionário com todos os DataFrames
dataframes = {
    'df_total': df_total,
    'df_receita_total': df_receita_total,
    'df_vendas_mes': df_vendas_mes,
    'df_modelos_vendidos': df_modelos_vendidos,
    'df_sazonalidade': df_sazonalidade,
    'df_agrupar_faixa_renda': df_agrupar_faixa_renda,
    'df_genero': df_genero,
    'df_renda_x_modelo': df_renda_x_modelo,
    'df_preferencias': df_preferencias,
    'df_receita_regiao': df_receita_regiao,
    'df_ticket_medio_concessionaria': df_ticket_medio_concessionaria,
    'df_ranking': df_ranking,
    'df_comparacao_regioes': df_comparacao_regioes,
    'df_body_style': df_body_style,
    'df_transmission': df_transmission,
    'df_color': df_color,
    'df_top_marcas': df_top_marcas,
    'df_evolucao': df_evolucao,
    'df_correlacao': df_correlacao,
    'df_original': df
}

# Salvar como pickle para uso no Streamlit
with open('dataframes.pkl', 'wb') as f:
    pickle.dump(dataframes, f)

# Salvar também como CSV individuais
import os
os.makedirs('dataframes_csv', exist_ok=True)

for name, data in dataframes.items():
    if name != 'df_original':  # Não salvar o original novamente
        data.to_csv(f'dataframes_csv/{name}.csv', index=False)

print("✓ DataFrames salvos em 'dataframes.pkl' e 'dataframes_csv/'")

# ============================================================================
# RESUMO
# ============================================================================

print("\n" + "="*80)
print("RESUMO DOS DATAFRAMES GERADOS")
print("="*80)

for name, data in dataframes.items():
    if isinstance(data, pd.DataFrame):
        print(f"\n{name}:")
        print(f"  • Shape: {data.shape}")
        print(f"  • Colunas: {list(data.columns)}")

print("\n" + "="*80)
print("✓ PROCESSO CONCLUÍDO COM SUCESSO!")
print("="*80)
