"""
============================================================================
PROJETO INTEGRADOR - APOIO DECISÓRIO AOS NEGÓCIOS
Script de Homepage Streamlit
Autor: Aline Morais
Data: 12/11/2025
Descrição: Script Python para utilizar o streamlit
============================================================================
"""

import streamlit as st

# Configurações da página
st.set_page_config(
    page_title="Dashboard Car Sales",
    page_icon="🚗",
)

# Título da página
st.write("# Dashboard Car Sales 🚗")

# Barra lateral
st.sidebar.success("Escolha uma da opções.")

# Conteúdo da página
st.markdown(
    """
    O setor automotivo desempenha um papel estratégico na economia global, 
    exigindo constantes adaptações diante de transformações tecnológicas, 
    mudanças de mercado e novos perfis de consumo. Nesse contexto, 
    a análise de dados surge como ferramenta essencial para apoiar a 
    tomada de decisão e aumentar a competitividade das organizações. 
    Este trabalho apresenta uma proposta de aplicação de Business Intelligence (BI) 
    no setor automotivo, utilizando como base o Car Sales Report Dataset, 
    disponibilizado na plataforma Kaggle.
    """
)

# Imagem ilustrativa
st.image("imagens/car-factory.png", 
         caption="Automação industrial na fabricação de veículos", 
         use_column_width=True
         )

# Notas finais

st.markdown(
    """
    Ao utilizar ferramentas de BI e técnicas de análise de dados aplicadas a 
    bancos de dados estruturados, este estudo demonstra como informações históricas e
    operacionais podem ser transformadas em insights estratégicos. Através da construção
    de um dashboard interativo em Streamlit, busca-se evidenciar o potencial da visualização 
    analítica para suportar gestores na identificação de tendências, monitoramento de 
    desempenho e direcionamento de ações mais assertivas no setor automotivo.
    """
)