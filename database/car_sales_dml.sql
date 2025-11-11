-- ============================================================================
-- PROJETO INTEGRADOR - APOIO DECISÓRIO AOS NEGÓCIOS
-- Script DML (Data Manipulation Language)
-- Banco de Dados: MySQL
-- Autor: David Carvalho
-- Data: 10/11/2025
-- Descrição: Carga de dados e operações de manipulação
-- ============================================================================

USE car_sales_db;

-- ============================================================================
-- PARTE 1: CARGA DE DADOS NA TABELA PRINCIPAL
-- ============================================================================

-- NOTA: A carga dos dados do CSV será feita via Python/Pandas ou LOAD DATA INFILE
-- Este script contém exemplos de INSERT e operações DML para demonstração

-- Exemplo de INSERT manual (os dados reais virão do CSV via script Python)
-- INSERT INTO car_sales VALUES
-- ('C_CND_000001', '2022-01-02', 'Geraldine', 'Male', 13500.00, 8264678, 
--  'Buddy Storbeck''s Diesel Service Inc', '06457-3834', 'Middletown',
--  'Ford', 'Expedition', 'SUV', 'DoubleÂ Overhead Camshaft', 'Auto', 'Black', 26000.00);

-- ============================================================================
-- PARTE 2: POPULAR DIMENSÕES PARA MODELO STAR SCHEMA
-- ============================================================================

-- Popular Dimensão Tempo
INSERT INTO dim_time (date_key, day, month, quarter, year, month_name, quarter_name, day_of_week, day_name, is_weekend)
SELECT DISTINCT
    sale_date AS date_key,
    DAY(sale_date) AS day,
    MONTH(sale_date) AS month,
    QUARTER(sale_date) AS quarter,
    YEAR(sale_date) AS year,
    DATE_FORMAT(sale_date, '%M') AS month_name,
    CONCAT('Q', QUARTER(sale_date)) AS quarter_name,
    DAYOFWEEK(sale_date) AS day_of_week,
    DATE_FORMAT(sale_date, '%W') AS day_name,
    CASE WHEN DAYOFWEEK(sale_date) IN (1, 7) THEN TRUE ELSE FALSE END AS is_weekend
FROM car_sales
ORDER BY sale_date;

-- Popular Dimensão Cliente
INSERT INTO dim_customer (customer_name, gender, income_bracket, annual_income, phone)
SELECT DISTINCT
    customer_name,
    gender,
    CASE 
        WHEN annual_income < 50000 THEN 'Baixa (< 50k)'
        WHEN annual_income BETWEEN 50000 AND 100000 THEN 'Média-Baixa (50k-100k)'
        WHEN annual_income BETWEEN 100001 AND 500000 THEN 'Média (100k-500k)'
        WHEN annual_income BETWEEN 500001 AND 1000000 THEN 'Média-Alta (500k-1M)'
        ELSE 'Alta (> 1M)'
    END AS income_bracket,
    annual_income,
    phone
FROM car_sales;

-- Popular Dimensão Concessionária
INSERT INTO dim_dealer (dealer_name, dealer_no, dealer_region)
SELECT DISTINCT
    dealer_name,
    dealer_no,
    dealer_region
FROM car_sales;

-- Popular Dimensão Veículo
INSERT INTO dim_vehicle (company, model, body_style, engine, transmission, color)
SELECT DISTINCT
    company,
    model,
    body_style,
    engine,
    transmission,
    color
FROM car_sales;

-- Popular Tabela Fato
INSERT INTO fact_sales (car_id, date_key, customer_key, dealer_key, vehicle_key, price, annual_income, financial_effort_ratio)
SELECT 
    cs.car_id,
    cs.sale_date,
    dc.customer_key,
    dd.dealer_key,
    dv.vehicle_key,
    cs.price,
    cs.annual_income,
    CASE 
        WHEN cs.annual_income > 0 THEN cs.price / cs.annual_income 
        ELSE NULL 
    END AS financial_effort_ratio
FROM car_sales cs
LEFT JOIN dim_customer dc ON cs.customer_name = dc.customer_name 
    AND cs.gender = dc.gender 
    AND cs.annual_income = dc.annual_income
LEFT JOIN dim_dealer dd ON cs.dealer_name = dd.dealer_name 
    AND cs.dealer_region = dd.dealer_region
LEFT JOIN dim_vehicle dv ON cs.company = dv.company 
    AND cs.model = dv.model 
    AND cs.body_style = dv.body_style
    AND cs.engine = dv.engine
    AND cs.transmission = dv.transmission
    AND cs.color = dv.color;

-- ============================================================================
-- PARTE 3: OPERAÇÕES OLAP - CONSULTAS ANALÍTICAS
-- ============================================================================

-- ============================================================================
-- OLAP 1: ANÁLISE DE VENDAS E DESEMPENHO COMERCIAL
-- ============================================================================

-- Volume de vendas por mês
SELECT 
    year_month,
    total_sales_volume,
    total_revenue,
    average_ticket
FROM vw_sales_performance
ORDER BY year_month;

-- Taxa de crescimento mensal
SELECT 
    year_month,
    total_revenue,
    LAG(total_revenue) OVER (ORDER BY year_month) AS previous_month_revenue,
    ROUND(
        ((total_revenue - LAG(total_revenue) OVER (ORDER BY year_month)) / 
        LAG(total_revenue) OVER (ORDER BY year_month)) * 100, 2
    ) AS growth_rate_percentage
FROM vw_sales_performance
ORDER BY year_month;

-- Modelos e marcas mais vendidos
SELECT 
    company,
    model,
    sales_count,
    total_revenue,
    average_price
FROM vw_sales_by_model
ORDER BY sales_count DESC
LIMIT 20;

-- Análise de sazonalidade (vendas por trimestre)
SELECT 
    year,
    quarter,
    SUM(total_sales_volume) AS quarterly_sales,
    SUM(total_revenue) AS quarterly_revenue,
    AVG(average_ticket) AS avg_quarterly_ticket
FROM vw_sales_performance
GROUP BY year, quarter
ORDER BY year, quarter;

-- ============================================================================
-- OLAP 2: PERFIL DO CLIENTE
-- ============================================================================

-- Distribuição de clientes por faixa de renda
SELECT 
    income_bracket,
    SUM(customer_count) AS total_customers,
    ROUND(SUM(customer_count) * 100.0 / (SELECT SUM(customer_count) FROM vw_customer_profile), 2) AS percentage,
    AVG(avg_purchase_price) AS avg_price,
    AVG(avg_income) AS avg_income
FROM vw_customer_profile
GROUP BY income_bracket
ORDER BY avg_income;

-- Percentual de vendas por gênero
SELECT 
    gender,
    COUNT(car_id) AS sales_count,
    ROUND(COUNT(car_id) * 100.0 / (SELECT COUNT(*) FROM car_sales), 2) AS percentage,
    AVG(price) AS avg_purchase_price,
    AVG(annual_income) AS avg_income
FROM car_sales
GROUP BY gender;

-- Índice de esforço financeiro por faixa de renda
SELECT 
    income_bracket,
    gender,
    AVG(financial_effort_index) AS avg_financial_effort,
    COUNT(*) AS customer_count
FROM vw_customer_profile
GROUP BY income_bracket, gender
ORDER BY income_bracket, gender;

-- Preferências de veículos por faixa de renda
SELECT 
    income_bracket,
    company,
    model,
    purchase_count,
    avg_price
FROM vw_income_preferences
WHERE purchase_count > 10
ORDER BY income_bracket, purchase_count DESC;

-- ============================================================================
-- OLAP 3: ANÁLISE REGIONAL
-- ============================================================================

-- Receita total por região
SELECT 
    dealer_region,
    SUM(sales_volume) AS total_sales,
    SUM(total_revenue) AS total_revenue,
    AVG(average_ticket) AS avg_ticket,
    ROUND(SUM(total_revenue) * 100.0 / (SELECT SUM(price) FROM car_sales), 2) AS revenue_percentage
FROM vw_regional_analysis
GROUP BY dealer_region
ORDER BY total_revenue DESC;

-- Ticket médio por concessionária
SELECT 
    dealer_name,
    dealer_region,
    sales_volume,
    total_revenue,
    average_ticket
FROM vw_regional_analysis
ORDER BY average_ticket DESC
LIMIT 20;

-- Ranking de concessionárias por volume e receita
SELECT 
    ranking_volume,
    ranking_revenue,
    dealer_name,
    dealer_region,
    sales_volume,
    total_revenue,
    average_ticket
FROM vw_dealer_ranking
ORDER BY ranking_volume
LIMIT 20;

-- Comparação entre regiões
SELECT 
    dealer_region,
    COUNT(DISTINCT dealer_name) AS num_dealers,
    SUM(sales_volume) AS total_sales,
    SUM(total_revenue) AS total_revenue,
    AVG(average_ticket) AS avg_ticket,
    SUM(total_revenue) / COUNT(DISTINCT dealer_name) AS revenue_per_dealer
FROM vw_regional_analysis
GROUP BY dealer_region
ORDER BY total_revenue DESC;

-- ============================================================================
-- OLAP 4: ANÁLISES AVANÇADAS COM DRILL-DOWN E ROLL-UP
-- ============================================================================

-- Drill-Down: Análise detalhada por Região > Concessionária > Mês
SELECT 
    cs.dealer_region,
    cs.dealer_name,
    DATE_FORMAT(cs.sale_date, '%Y-%m') AS year_month,
    COUNT(cs.car_id) AS sales_count,
    SUM(cs.price) AS revenue,
    AVG(cs.price) AS avg_ticket
FROM car_sales cs
GROUP BY cs.dealer_region, cs.dealer_name, year_month
WITH ROLLUP
ORDER BY cs.dealer_region, cs.dealer_name, year_month;

-- Roll-Up: Agregação por Ano > Trimestre > Mês
SELECT 
    YEAR(sale_date) AS year,
    QUARTER(sale_date) AS quarter,
    MONTH(sale_date) AS month,
    COUNT(car_id) AS sales_volume,
    SUM(price) AS total_revenue,
    AVG(price) AS avg_ticket
FROM car_sales
GROUP BY year, quarter, month WITH ROLLUP
ORDER BY year, quarter, month;

-- Slice: Análise específica de uma região
SELECT 
    dealer_name,
    company,
    model,
    COUNT(car_id) AS sales_count,
    SUM(price) AS revenue
FROM car_sales
WHERE dealer_region = 'Austin'
GROUP BY dealer_name, company, model
ORDER BY sales_count DESC;

-- Dice: Análise multidimensional (Região + Gênero + Faixa de Renda)
SELECT 
    dealer_region,
    gender,
    CASE 
        WHEN annual_income < 50000 THEN 'Baixa'
        WHEN annual_income BETWEEN 50000 AND 500000 THEN 'Média'
        ELSE 'Alta'
    END AS income_level,
    COUNT(car_id) AS sales_count,
    AVG(price) AS avg_price,
    SUM(price) AS total_revenue
FROM car_sales
WHERE dealer_region IN ('Austin', 'Pasco', 'Aurora')
    AND gender IN ('Male', 'Female')
GROUP BY dealer_region, gender, income_level
ORDER BY dealer_region, gender, income_level;

-- Pivot: Análise de vendas por região e trimestre
SELECT 
    dealer_region,
    SUM(CASE WHEN QUARTER(sale_date) = 1 THEN price ELSE 0 END) AS Q1_revenue,
    SUM(CASE WHEN QUARTER(sale_date) = 2 THEN price ELSE 0 END) AS Q2_revenue,
    SUM(CASE WHEN QUARTER(sale_date) = 3 THEN price ELSE 0 END) AS Q3_revenue,
    SUM(CASE WHEN QUARTER(sale_date) = 4 THEN price ELSE 0 END) AS Q4_revenue,
    SUM(price) AS total_revenue
FROM car_sales
GROUP BY dealer_region
ORDER BY total_revenue DESC;

-- ============================================================================
-- PARTE 4: OPERAÇÕES DE ATUALIZAÇÃO E MANUTENÇÃO
-- ============================================================================

-- Atualizar preços (exemplo de UPDATE)
-- UPDATE car_sales 
-- SET price = price * 1.05 
-- WHERE YEAR(sale_date) = 2022 AND MONTH(sale_date) = 1;

-- Deletar registros inválidos (exemplo de DELETE)
-- DELETE FROM car_sales 
-- WHERE price <= 0 OR annual_income <= 0;

-- ============================================================================
-- PARTE 5: CONSULTAS DE VALIDAÇÃO E QUALIDADE DE DADOS
-- ============================================================================

-- Verificar integridade dos dados
SELECT 
    'Total de registros' AS metric,
    COUNT(*) AS value
FROM car_sales
UNION ALL
SELECT 
    'Registros com preço nulo' AS metric,
    COUNT(*) AS value
FROM car_sales
WHERE price IS NULL
UNION ALL
SELECT 
    'Registros com renda nula' AS metric,
    COUNT(*) AS value
FROM car_sales
WHERE annual_income IS NULL
UNION ALL
SELECT 
    'Registros duplicados' AS metric,
    COUNT(*) - COUNT(DISTINCT car_id) AS value
FROM car_sales;

-- Estatísticas gerais
SELECT 
    COUNT(DISTINCT car_id) AS total_sales,
    COUNT(DISTINCT customer_name) AS unique_customers,
    COUNT(DISTINCT dealer_name) AS total_dealers,
    COUNT(DISTINCT company) AS total_brands,
    COUNT(DISTINCT model) AS total_models,
    MIN(sale_date) AS first_sale_date,
    MAX(sale_date) AS last_sale_date,
    SUM(price) AS total_revenue,
    AVG(price) AS average_price,
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM car_sales;

-- ============================================================================
-- FIM DO SCRIPT DML
-- ============================================================================
