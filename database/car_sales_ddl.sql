-- ============================================================================
-- PROJETO INTEGRADOR - APOIO DECISÓRIO AOS NEGÓCIOS
-- Script DDL (Data Definition Language)
-- Banco de Dados: MySQL
-- Autor: David Carvalho
-- Data: 10/11/2025
-- Descrição: Criação do banco de dados e tabelas para análise de vendas de carros
-- ============================================================================

-- Criar o banco de dados se não existir
CREATE DATABASE IF NOT EXISTS car_sales_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Usar o banco de dados criado
USE car_sales_db;

-- Remover a tabela se já existir (para recriar)
DROP TABLE IF EXISTS car_sales;

-- Criar a tabela principal de vendas de carros
CREATE TABLE car_sales (
    -- Chave primária
    car_id VARCHAR(20) PRIMARY KEY COMMENT 'Identificador único do carro vendido',
    
    -- Informações da venda
    sale_date DATE NOT NULL COMMENT 'Data da venda',
    
    -- Informações do cliente
    customer_name VARCHAR(100) NOT NULL COMMENT 'Nome do cliente',
    gender ENUM('Male', 'Female') NOT NULL COMMENT 'Gênero do cliente',
    annual_income DECIMAL(12,2) NOT NULL COMMENT 'Renda anual do cliente em dólares',
    phone BIGINT COMMENT 'Telefone do cliente',
    
    -- Informações da concessionária
    dealer_name VARCHAR(100) NOT NULL COMMENT 'Nome da concessionária',
    dealer_no VARCHAR(20) COMMENT 'Número da concessionária',
    dealer_region VARCHAR(50) NOT NULL COMMENT 'Região da concessionária',
    
    -- Informações do veículo
    company VARCHAR(50) NOT NULL COMMENT 'Fabricante do veículo',
    model VARCHAR(100) NOT NULL COMMENT 'Modelo do veículo',
    body_style VARCHAR(30) NOT NULL COMMENT 'Estilo da carroceria',
    engine VARCHAR(50) NOT NULL COMMENT 'Tipo de motor',
    transmission VARCHAR(20) NOT NULL COMMENT 'Tipo de transmissão',
    color VARCHAR(30) NOT NULL COMMENT 'Cor do veículo',
    
    -- Informações financeiras
    price DECIMAL(10,2) NOT NULL COMMENT 'Preço de venda em dólares',
    
    -- Índices para otimização de consultas
    INDEX idx_sale_date (sale_date),
    INDEX idx_dealer_region (dealer_region),
    INDEX idx_dealer_name (dealer_name),
    INDEX idx_company (company),
    INDEX idx_model (model),
    INDEX idx_gender (gender),
    INDEX idx_price (price),
    INDEX idx_annual_income (annual_income)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Tabela principal de vendas de carros para análise OLAP';

-- ============================================================================
-- VIEWS PARA OPERAÇÕES OLAP
-- ============================================================================

-- View 1: Análise de Vendas e Desempenho Comercial
DROP VIEW IF EXISTS vw_sales_performance;
CREATE VIEW vw_sales_performance AS
SELECT 
    DATE_FORMAT(sale_date, '%Y-%m') AS year_month,
    YEAR(sale_date) AS year,
    MONTH(sale_date) AS month,
    QUARTER(sale_date) AS quarter,
    COUNT(car_id) AS total_sales_volume,
    SUM(price) AS total_revenue,
    AVG(price) AS average_ticket,
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM car_sales
GROUP BY year_month, year, month, quarter
ORDER BY year_month;

-- View 2: Análise por Modelo e Marca
DROP VIEW IF EXISTS vw_sales_by_model;
CREATE VIEW vw_sales_by_model AS
SELECT 
    company,
    model,
    COUNT(car_id) AS sales_count,
    SUM(price) AS total_revenue,
    AVG(price) AS average_price,
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM car_sales
GROUP BY company, model
ORDER BY sales_count DESC;

-- View 3: Análise Regional
DROP VIEW IF EXISTS vw_regional_analysis;
CREATE VIEW vw_regional_analysis AS
SELECT 
    dealer_region,
    dealer_name,
    COUNT(car_id) AS sales_volume,
    SUM(price) AS total_revenue,
    AVG(price) AS average_ticket,
    ROUND(SUM(price) * 100.0 / (SELECT SUM(price) FROM car_sales), 2) AS revenue_percentage
FROM car_sales
GROUP BY dealer_region, dealer_name
ORDER BY total_revenue DESC;

-- View 4: Perfil do Cliente
DROP VIEW IF EXISTS vw_customer_profile;
CREATE VIEW vw_customer_profile AS
SELECT 
    gender,
    CASE 
        WHEN annual_income < 50000 THEN 'Baixa (< 50k)'
        WHEN annual_income BETWEEN 50000 AND 100000 THEN 'Média-Baixa (50k-100k)'
        WHEN annual_income BETWEEN 100001 AND 500000 THEN 'Média (100k-500k)'
        WHEN annual_income BETWEEN 500001 AND 1000000 THEN 'Média-Alta (500k-1M)'
        ELSE 'Alta (> 1M)'
    END AS income_bracket,
    COUNT(car_id) AS customer_count,
    AVG(price) AS avg_purchase_price,
    AVG(annual_income) AS avg_income,
    AVG(price / annual_income) AS financial_effort_index
FROM car_sales
GROUP BY gender, income_bracket
ORDER BY gender, avg_income;

-- View 5: Análise de Preferências por Renda
DROP VIEW IF EXISTS vw_income_preferences;
CREATE VIEW vw_income_preferences AS
SELECT 
    CASE 
        WHEN annual_income < 50000 THEN 'Baixa (< 50k)'
        WHEN annual_income BETWEEN 50000 AND 100000 THEN 'Média-Baixa (50k-100k)'
        WHEN annual_income BETWEEN 100001 AND 500000 THEN 'Média (100k-500k)'
        WHEN annual_income BETWEEN 500001 AND 1000000 THEN 'Média-Alta (500k-1M)'
        ELSE 'Alta (> 1M)'
    END AS income_bracket,
    company,
    model,
    body_style,
    COUNT(car_id) AS purchase_count,
    AVG(price) AS avg_price
FROM car_sales
GROUP BY income_bracket, company, model, body_style
ORDER BY income_bracket, purchase_count DESC;

-- View 6: Ranking de Concessionárias
DROP VIEW IF EXISTS vw_dealer_ranking;
CREATE VIEW vw_dealer_ranking AS
SELECT 
    RANK() OVER (ORDER BY COUNT(car_id) DESC) AS ranking_volume,
    RANK() OVER (ORDER BY SUM(price) DESC) AS ranking_revenue,
    dealer_name,
    dealer_region,
    COUNT(car_id) AS sales_volume,
    SUM(price) AS total_revenue,
    AVG(price) AS average_ticket
FROM car_sales
GROUP BY dealer_name, dealer_region
ORDER BY sales_volume DESC;

-- ============================================================================
-- TABELAS DIMENSIONAIS PARA ANÁLISE OLAP (STAR SCHEMA)
-- ============================================================================

-- Dimensão Tempo
DROP TABLE IF EXISTS dim_time;
CREATE TABLE dim_time (
    date_key DATE PRIMARY KEY,
    day INT NOT NULL,
    month INT NOT NULL,
    quarter INT NOT NULL,
    year INT NOT NULL,
    month_name VARCHAR(20),
    quarter_name VARCHAR(10),
    day_of_week INT,
    day_name VARCHAR(20),
    is_weekend BOOLEAN,
    INDEX idx_year_month (year, month),
    INDEX idx_quarter (year, quarter)
) ENGINE=InnoDB COMMENT='Dimensão temporal para análise OLAP';

-- Dimensão Cliente
DROP TABLE IF EXISTS dim_customer;
CREATE TABLE dim_customer (
    customer_key INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    gender ENUM('Male', 'Female'),
    income_bracket VARCHAR(50),
    annual_income DECIMAL(12,2),
    phone BIGINT,
    INDEX idx_gender (gender),
    INDEX idx_income_bracket (income_bracket)
) ENGINE=InnoDB COMMENT='Dimensão cliente para análise OLAP';

-- Dimensão Concessionária
DROP TABLE IF EXISTS dim_dealer;
CREATE TABLE dim_dealer (
    dealer_key INT AUTO_INCREMENT PRIMARY KEY,
    dealer_name VARCHAR(100),
    dealer_no VARCHAR(20),
    dealer_region VARCHAR(50),
    INDEX idx_dealer_name (dealer_name),
    INDEX idx_dealer_region (dealer_region)
) ENGINE=InnoDB COMMENT='Dimensão concessionária para análise OLAP';

-- Dimensão Veículo
DROP TABLE IF EXISTS dim_vehicle;
CREATE TABLE dim_vehicle (
    vehicle_key INT AUTO_INCREMENT PRIMARY KEY,
    company VARCHAR(50),
    model VARCHAR(100),
    body_style VARCHAR(30),
    engine VARCHAR(50),
    transmission VARCHAR(20),
    color VARCHAR(30),
    INDEX idx_company (company),
    INDEX idx_model (model),
    INDEX idx_body_style (body_style)
) ENGINE=InnoDB COMMENT='Dimensão veículo para análise OLAP';

-- Tabela Fato - Vendas
DROP TABLE IF EXISTS fact_sales;
CREATE TABLE fact_sales (
    sale_key INT AUTO_INCREMENT PRIMARY KEY,
    car_id VARCHAR(20) UNIQUE,
    date_key DATE NOT NULL,
    customer_key INT,
    dealer_key INT,
    vehicle_key INT,
    price DECIMAL(10,2) NOT NULL,
    annual_income DECIMAL(12,2) NOT NULL,
    financial_effort_ratio DECIMAL(10,6),
    
    FOREIGN KEY (date_key) REFERENCES dim_time(date_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (dealer_key) REFERENCES dim_dealer(dealer_key),
    FOREIGN KEY (vehicle_key) REFERENCES dim_vehicle(vehicle_key),
    
    INDEX idx_date (date_key),
    INDEX idx_customer (customer_key),
    INDEX idx_dealer (dealer_key),
    INDEX idx_vehicle (vehicle_key),
    INDEX idx_price (price)
) ENGINE=InnoDB COMMENT='Tabela fato de vendas para análise OLAP';

-- ============================================================================
-- FIM DO SCRIPT DDL
-- ============================================================================
