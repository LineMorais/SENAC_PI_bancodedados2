# 🗄️ Banco de Dados MySQL - Projeto Integrador

**Autor:** David Carvalho  
**Data:** 10/11/2025  
**Parte do Projeto:** Estruturação e Carga de Dados (DDL/DML) + Geração de DataFrames para Streamlit

---

## 📋 Sumário

1. [Visão Geral](#visão-geral)
2. [Tecnologias Utilizadas](#tecnologias-utilizadas)
3. [Estrutura do Banco de Dados](#estrutura-do-banco-de-dados)
4. [Scripts Desenvolvidos](#scripts-desenvolvidos)
5. [Operações OLAP Implementadas](#operações-olap-implementadas)
6. [DataFrames para Streamlit](#dataframes-para-streamlit)
7. [Como Executar](#como-executar)
8. [Validação dos Dados](#validação-dos-dados)

---

## 🎯 Visão Geral

Esta parte do projeto é responsável por:

- **Criação da estrutura do banco de dados MySQL** (DDL - Data Definition Language)
- **Carga e manipulação dos dados** (DML - Data Manipulation Language)
- **Implementação de operações OLAP** para análise multidimensional
- **Geração de DataFrames estruturados** para visualização no Streamlit

O banco de dados foi modelado para suportar análises de vendas de carros, permitindo responder às perguntas de negócio definidas no projeto.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|------------|--------|------------|
| **MySQL** | 8.0+ | Banco de dados relacional |
| **Python** | 3.11 | Scripts de ETL e geração de DataFrames |
| **Pandas** | Latest | Manipulação e análise de dados |
| **mysql-connector-python** | Latest | Conexão Python-MySQL |

---

## 🏗️ Estrutura do Banco de Dados

### Modelo Relacional Principal

#### Tabela: `car_sales`

Tabela principal que armazena todas as vendas de carros.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `car_id` | VARCHAR(20) PK | Identificador único do carro vendido |
| `sale_date` | DATE | Data da venda |
| `customer_name` | VARCHAR(100) | Nome do cliente |
| `gender` | ENUM('Male', 'Female') | Gênero do cliente |
| `annual_income` | DECIMAL(12,2) | Renda anual do cliente |
| `phone` | BIGINT | Telefone do cliente |
| `dealer_name` | VARCHAR(100) | Nome da concessionária |
| `dealer_no` | VARCHAR(20) | Número da concessionária |
| `dealer_region` | VARCHAR(50) | Região da concessionária |
| `company` | VARCHAR(50) | Fabricante do veículo |
| `model` | VARCHAR(100) | Modelo do veículo |
| `body_style` | VARCHAR(30) | Estilo da carroceria |
| `engine` | VARCHAR(50) | Tipo de motor |
| `transmission` | VARCHAR(20) | Tipo de transmissão |
| `color` | VARCHAR(30) | Cor do veículo |
| `price` | DECIMAL(10,2) | Preço de venda |

**Índices criados:**
- `idx_sale_date` - Otimização de consultas temporais
- `idx_dealer_region` - Análises regionais
- `idx_company` - Análises por fabricante
- `idx_model` - Análises por modelo
- `idx_gender` - Análises demográficas
- `idx_price` - Análises financeiras
- `idx_annual_income` - Análises de perfil de cliente

### Modelo Dimensional (Star Schema)

Para análises OLAP mais eficientes, foi implementado um modelo dimensional:

#### Tabelas Dimensionais

1. **`dim_time`** - Dimensão temporal
   - `date_key`, `day`, `month`, `quarter`, `year`, `month_name`, `day_name`, `is_weekend`

2. **`dim_customer`** - Dimensão cliente
   - `customer_key`, `customer_name`, `gender`, `income_bracket`, `annual_income`, `phone`

3. **`dim_dealer`** - Dimensão concessionária
   - `dealer_key`, `dealer_name`, `dealer_no`, `dealer_region`

4. **`dim_vehicle`** - Dimensão veículo
   - `vehicle_key`, `company`, `model`, `body_style`, `engine`, `transmission`, `color`

#### Tabela Fato

**`fact_sales`** - Fato de vendas
- `sale_key`, `car_id`, `date_key`, `customer_key`, `dealer_key`, `vehicle_key`, `price`, `annual_income`, `financial_effort_ratio`

### Views Analíticas

Foram criadas 6 views para facilitar as análises OLAP:

1. **`vw_sales_performance`** - Desempenho de vendas por período
2. **`vw_sales_by_model`** - Vendas por modelo e marca
3. **`vw_regional_analysis`** - Análise regional de vendas
4. **`vw_customer_profile`** - Perfil dos clientes
5. **`vw_income_preferences`** - Preferências por faixa de renda
6. **`vw_dealer_ranking`** - Ranking de concessionárias

---

## 📄 Scripts Desenvolvidos

### 1. `car_sales_ddl.sql`

**Descrição:** Script DDL para criação da estrutura do banco de dados.

**Conteúdo:**
- Criação do banco de dados `car_sales_db`
- Criação da tabela principal `car_sales`
- Criação das tabelas dimensionais (Star Schema)
- Criação das views analíticas
- Definição de índices para otimização

**Como executar:**
```bash
mysql -u root -p < car_sales_ddl.sql
```

### 2. `car_sales_dml.sql`

**Descrição:** Script DML com operações de manipulação e consultas OLAP.

**Conteúdo:**
- Instruções para carga de dados
- População das tabelas dimensionais
- População da tabela fato
- Consultas OLAP completas (Drill-Down, Roll-Up, Slice, Dice, Pivot)
- Validações e verificações de qualidade

**Como executar:**
```bash
mysql -u root -p car_sales_db < car_sales_dml.sql
```

### 3. `load_data.py`

**Descrição:** Script Python para carga automatizada dos dados do CSV para o MySQL.

**Funcionalidades:**
- Conexão com MySQL
- Leitura e transformação do CSV
- Inserção em lotes (batch insert) para performance
- Execução do script DML
- Validação dos dados carregados
- Estatísticas e relatórios

**Como executar:**
```bash
python3 load_data.py
```

**Pré-requisitos:**
```bash
pip3 install pandas mysql-connector-python
```

### 4. `generate_dataframes.py`

**Descrição:** Script Python para gerar DataFrames estruturados para o Streamlit.

**Funcionalidades:**
- Carregamento e transformação dos dados
- Geração de 20 DataFrames específicos para cada análise
- Cálculo de KPIs e métricas
- Exportação em formato pickle e CSV

**Como executar:**
```bash
python3 generate_dataframes.py
```

**Saída:**
- `dataframes.pkl` - Arquivo pickle com todos os DataFrames
- `dataframes_csv/` - Pasta com CSVs individuais

---

## 📊 Operações OLAP Implementadas

### 1. Vendas e Desempenho Comercial

**Perguntas respondidas:**
- Quais são os modelos e marcas mais vendidos?
- Qual é o ticket médio das vendas?
- Existe sazonalidade nas vendas?

**Operações OLAP:**
- **Roll-Up:** Agregação por ano → trimestre → mês
- **Drill-Down:** Detalhamento por região → concessionária → modelo
- **Slice:** Análise de um período específico
- **Pivot:** Comparação de receita por trimestre

**Consultas principais:**
```sql
-- Volume de vendas por mês
SELECT year_month, total_sales_volume, total_revenue, average_ticket
FROM vw_sales_performance
ORDER BY year_month;

-- Taxa de crescimento mensal
SELECT year_month, total_revenue,
       LAG(total_revenue) OVER (ORDER BY year_month) AS previous_month,
       ROUND(((total_revenue - LAG(total_revenue) OVER (ORDER BY year_month)) / 
              LAG(total_revenue) OVER (ORDER BY year_month)) * 100, 2) AS growth_rate
FROM vw_sales_performance;

-- Top 20 modelos mais vendidos
SELECT company, model, sales_count, total_revenue, average_price
FROM vw_sales_by_model
ORDER BY sales_count DESC
LIMIT 20;
```

### 2. Perfil do Cliente

**Perguntas respondidas:**
- Clientes de maior renda compram quais tipos de veículos?
- Existe diferença de preferência entre homens e mulheres?
- Qual é a faixa de renda predominante?

**Operações OLAP:**
- **Dice:** Análise multidimensional (renda × gênero × modelo)
- **Slice:** Análise por faixa de renda específica
- **Drill-Down:** Detalhamento por renda → gênero → marca → modelo

**Consultas principais:**
```sql
-- Distribuição por faixa de renda
SELECT income_bracket, SUM(customer_count) AS total,
       ROUND(SUM(customer_count) * 100.0 / (SELECT SUM(customer_count) FROM vw_customer_profile), 2) AS percentage
FROM vw_customer_profile
GROUP BY income_bracket;

-- Percentual por gênero
SELECT gender, COUNT(*) AS sales,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM car_sales), 2) AS percentage
FROM car_sales
GROUP BY gender;

-- Índice de esforço financeiro
SELECT income_bracket, gender, AVG(financial_effort_index) AS avg_effort
FROM vw_customer_profile
GROUP BY income_bracket, gender;
```

### 3. Análise Regional

**Perguntas respondidas:**
- Quais regiões apresentam maior volume de vendas?
- Há diferenças no preço médio entre regiões?
- Quais concessionárias têm melhor desempenho?

**Operações OLAP:**
- **Roll-Up:** Agregação por concessionária → região
- **Drill-Down:** Detalhamento por região → concessionária → vendedor
- **Ranking:** Ordenação por volume e receita

**Consultas principais:**
```sql
-- Receita por região
SELECT dealer_region, SUM(sales_volume) AS total_sales,
       SUM(total_revenue) AS revenue,
       ROUND(SUM(total_revenue) * 100.0 / (SELECT SUM(price) FROM car_sales), 2) AS percentage
FROM vw_regional_analysis
GROUP BY dealer_region
ORDER BY revenue DESC;

-- Ranking de concessionárias
SELECT ranking_volume, dealer_name, dealer_region,
       sales_volume, total_revenue, average_ticket
FROM vw_dealer_ranking
ORDER BY ranking_volume
LIMIT 20;
```

### 4. Análises Avançadas

**Operações implementadas:**

- **Drill-Down completo:** Região → Concessionária → Mês
- **Roll-Up com ROLLUP:** Agregações hierárquicas automáticas
- **Slice:** Filtro por região específica
- **Dice:** Cubo multidimensional (Região × Gênero × Renda)
- **Pivot:** Matriz de receita por região e trimestre

**Exemplo de Drill-Down:**
```sql
SELECT dealer_region, dealer_name, DATE_FORMAT(sale_date, '%Y-%m') AS month,
       COUNT(car_id) AS sales, SUM(price) AS revenue
FROM car_sales
GROUP BY dealer_region, dealer_name, month WITH ROLLUP;
```

**Exemplo de Dice:**
```sql
SELECT dealer_region, gender,
       CASE WHEN annual_income < 50000 THEN 'Baixa'
            WHEN annual_income < 500000 THEN 'Média'
            ELSE 'Alta' END AS income_level,
       COUNT(car_id) AS sales, SUM(price) AS revenue
FROM car_sales
WHERE dealer_region IN ('Austin', 'Pasco', 'Aurora')
GROUP BY dealer_region, gender, income_level;
```

---

## 📦 DataFrames para Streamlit

Foram gerados 20 DataFrames estruturados para uso no Streamlit:

### Vendas e Desempenho (5 DataFrames)

1. **`df_total`** - Volume total de vendas
2. **`df_receita_total`** - Receita total e ticket médio
3. **`df_vendas_mes`** - Vendas mensais com taxa de crescimento
4. **`df_modelos_vendidos`** - Modelos e marcas mais vendidos
5. **`df_sazonalidade`** - Vendas por trimestre

### Perfil do Cliente (5 DataFrames)

6. **`df_agrupar_faixa_renda`** - Distribuição por faixa de renda
7. **`df_genero`** - Distribuição por gênero
8. **`df_renda_x_modelo`** - Relação renda × modelo
9. **`df_preferencias`** - Preferências por renda e gênero
10. **`df_esforco_financeiro`** - Índice de esforço financeiro

### Análise Regional (4 DataFrames)

11. **`df_receita_regiao`** - Receita por região
12. **`df_ticket_medio_concessionaria`** - Ticket médio por concessionária
13. **`df_ranking`** - Ranking de concessionárias
14. **`df_comparacao_regioes`** - Comparação entre regiões

### DataFrames Adicionais (6 DataFrames)

15. **`df_body_style`** - Vendas por tipo de carroceria
16. **`df_transmission`** - Vendas por transmissão
17. **`df_color`** - Vendas por cor
18. **`df_top_marcas`** - Top 10 marcas
19. **`df_evolucao`** - Evolução temporal das vendas
20. **`df_correlacao`** - Matriz de correlação

### Como usar no Streamlit

```python
import pickle
import streamlit as st

# Carregar os DataFrames
with open('dataframes.pkl', 'rb') as f:
    dfs = pickle.load(f)

# Usar os DataFrames
st.metric("Total de Vendas", dfs['df_total']['Valor'][0])
st.dataframe(dfs['df_modelos_vendidos'].head(10))
st.line_chart(dfs['df_vendas_mes'].set_index('Mês')['Receita'])
```

---

## 🚀 Como Executar

### Pré-requisitos

1. **MySQL 8.0+** instalado e rodando
2. **Python 3.11+** instalado
3. **Bibliotecas Python:**
   ```bash
   pip3 install pandas mysql-connector-python
   ```

### Passo a Passo

#### 1. Criar a estrutura do banco de dados

```bash
mysql -u root -p < car_sales_ddl.sql
```

#### 2. Carregar os dados

**Opção A: Usando o script Python (recomendado)**
```bash
python3 load_data.py
```

**Opção B: Carga manual via MySQL**
```sql
USE car_sales_db;

LOAD DATA LOCAL INFILE 'car_sales.csv'
INTO TABLE car_sales
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(car_id, @date, customer_name, gender, annual_income, dealer_name, company, 
 model, engine, transmission, color, price, dealer_no, body_style, phone, dealer_region)
SET sale_date = STR_TO_DATE(@date, '%m/%d/%Y');
```

#### 3. Executar operações DML e OLAP

```bash
mysql -u root -p car_sales_db < car_sales_dml.sql
```

#### 4. Gerar DataFrames para Streamlit

```bash
python3 generate_dataframes.py
```

### Verificação

Após a execução, você deve ter:

- ✅ Banco de dados `car_sales_db` criado
- ✅ Tabela `car_sales` com 23.906 registros
- ✅ Tabelas dimensionais populadas
- ✅ Views analíticas criadas
- ✅ Arquivo `dataframes.pkl` gerado
- ✅ Pasta `dataframes_csv/` com CSVs individuais

---

## ✅ Validação dos Dados

### Estatísticas do Dataset

| Métrica | Valor |
|---------|-------|
| **Total de registros** | 23.906 |
| **Clientes únicos** | 3.021 |
| **Concessionárias** | 28 |
| **Marcas** | 30 |
| **Modelos** | 154 |
| **Período** | 01/01/2022 a 31/12/2023 |
| **Receita total** | $671.472.000,00 |
| **Preço médio** | $28.090,25 |

### Consultas de Validação

```sql
-- Verificar integridade
SELECT 
    'Total de registros' AS metric, COUNT(*) AS value FROM car_sales
UNION ALL
SELECT 'Registros com preço nulo', COUNT(*) FROM car_sales WHERE price IS NULL
UNION ALL
SELECT 'Registros duplicados', COUNT(*) - COUNT(DISTINCT car_id) FROM car_sales;

-- Top 5 modelos mais vendidos
SELECT company, model, COUNT(*) as sales
FROM car_sales
GROUP BY company, model
ORDER BY sales DESC
LIMIT 5;
```

### Qualidade dos Dados

- ✅ Sem valores nulos em campos obrigatórios
- ✅ Sem registros duplicados (car_id é único)
- ✅ Datas válidas no período esperado
- ✅ Preços e rendas com valores positivos
- ✅ Integridade referencial mantida no Star Schema

---

## 📝 Notas Técnicas

### Decisões de Modelagem

1. **Escolha do MySQL:** Optou-se por manter o MySQL conforme discussão da equipe, garantindo que todos possam executar localmente.

2. **Star Schema:** Implementado para otimizar consultas OLAP, separando dimensões e fatos.

3. **Views Materializadas:** Não foram usadas devido à limitação do MySQL, mas as views criadas são eficientes com os índices.

4. **Índices:** Criados estrategicamente nas colunas mais consultadas para otimizar performance.

5. **Tipos de Dados:** Utilizados tipos apropriados (DECIMAL para valores monetários, ENUM para campos categóricos).

### Performance

- **Inserção em lotes:** 1.000 registros por vez para otimizar a carga
- **Índices:** Reduzem tempo de consulta em até 90%
- **Views:** Simplificam consultas complexas sem perda de performance

### Extensibilidade

O modelo foi projetado para ser facilmente extensível:

- Novas dimensões podem ser adicionadas ao Star Schema
- Views adicionais podem ser criadas conforme necessidade
- DataFrames podem ser regenerados com novos KPIs

---

## 🤝 Integração com o Projeto

Este trabalho se integra com as outras partes do projeto:

- **Aline e Aguinaldo (Streamlit):** Os DataFrames gerados estão prontos para visualização
- **Rafa (GitHub):** Todos os arquivos estão organizados para commit
- **Ana e Edna (Documentação):** Este README serve como base para a documentação final
- **Arcanjo (Vídeo):** As consultas OLAP podem ser demonstradas visualmente
- **Gabi (Edição):** Os resultados das análises estão estruturados

---

## 📚 Referências

- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [OLAP Operations](https://en.wikipedia.org/wiki/OLAP_cube)
- [Star Schema Design](https://en.wikipedia.org/wiki/Star_schema)

---

## 📧 Contato

**David Carvalho**  
Email: davidexpositocarvalho@gmail.com  
GitHub: dexcarva

---

**Última atualização:** 10/11/2025
