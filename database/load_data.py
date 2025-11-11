#!/usr/bin/env python3
"""
============================================================================
PROJETO INTEGRADOR - APOIO DECISÓRIO AOS NEGÓCIOS
Script de Carga de Dados (ETL - Extract, Transform, Load)
Autor: David Carvalho
Data: 10/11/2025
Descrição: Script Python para carregar dados do CSV para o MySQL
============================================================================
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import sys

# Configurações do banco de dados
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Alterar conforme necessário
    'password': 'senha',  # Alterar conforme necessário
    'database': 'car_sales_db'
}

# Arquivo CSV de origem
CSV_FILE = 'car_sales.csv'


def create_connection():
    """Cria conexão com o banco de dados MySQL"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("✓ Conexão com MySQL estabelecida com sucesso")
            return connection
    except Error as e:
        print(f"✗ Erro ao conectar ao MySQL: {e}")
        return None


def load_csv_data(csv_file):
    """Carrega e transforma os dados do CSV"""
    try:
        print(f"\n→ Carregando dados do arquivo: {csv_file}")
        df = pd.read_csv(csv_file)
        
        print(f"✓ Dados carregados: {len(df)} registros")
        print(f"✓ Colunas: {list(df.columns)}")
        
        # Transformações necessárias
        print("\n→ Aplicando transformações nos dados...")
        
        # Converter data para formato MySQL
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
        
        # Limpar espaços em branco nas colunas
        df.columns = df.columns.str.strip()
        
        # Renomear colunas para corresponder ao schema do banco
        column_mapping = {
            'Car_id': 'car_id',
            'Date': 'sale_date',
            'Customer Name': 'customer_name',
            'Gender': 'gender',
            'Annual Income': 'annual_income',
            'Dealer_Name': 'dealer_name',
            'Company': 'company',
            'Model': 'model',
            'Engine': 'engine',
            'Transmission': 'transmission',
            'Color': 'color',
            'Price ($)': 'price',
            'Dealer_No': 'dealer_no',
            'Body Style': 'body_style',
            'Phone': 'phone',
            'Dealer_Region': 'dealer_region'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Tratar valores nulos
        df['phone'] = df['phone'].fillna(0)
        
        # Limpar strings
        for col in df.select_dtypes(include=['object']).columns:
            if col not in ['sale_date', 'car_id']:
                df[col] = df[col].str.strip()
        
        print("✓ Transformações aplicadas com sucesso")
        
        return df
        
    except Exception as e:
        print(f"✗ Erro ao carregar CSV: {e}")
        return None


def insert_data_batch(connection, df, batch_size=1000):
    """Insere dados no banco em lotes"""
    try:
        cursor = connection.cursor()
        
        # Query de inserção
        insert_query = """
        INSERT INTO car_sales (
            car_id, sale_date, customer_name, gender, annual_income, phone,
            dealer_name, dealer_no, dealer_region, company, model, body_style,
            engine, transmission, color, price
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        
        total_records = len(df)
        print(f"\n→ Iniciando inserção de {total_records} registros...")
        
        # Converter DataFrame para lista de tuplas
        records = []
        for _, row in df.iterrows():
            record = (
                row['car_id'],
                row['sale_date'].strftime('%Y-%m-%d'),
                row['customer_name'],
                row['gender'],
                float(row['annual_income']),
                int(row['phone']),
                row['dealer_name'],
                row['dealer_no'],
                row['dealer_region'],
                row['company'],
                row['model'],
                row['body_style'],
                row['engine'],
                row['transmission'],
                row['color'],
                float(row['price'])
            )
            records.append(record)
        
        # Inserir em lotes
        inserted = 0
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            cursor.executemany(insert_query, batch)
            connection.commit()
            inserted += len(batch)
            print(f"  → Inseridos {inserted}/{total_records} registros ({(inserted/total_records)*100:.1f}%)")
        
        print(f"✓ Total de {inserted} registros inseridos com sucesso!")
        
        cursor.close()
        return True
        
    except Error as e:
        print(f"✗ Erro ao inserir dados: {e}")
        connection.rollback()
        return False


def execute_sql_file(connection, sql_file):
    """Executa um arquivo SQL"""
    try:
        cursor = connection.cursor()
        
        print(f"\n→ Executando arquivo SQL: {sql_file}")
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Dividir por comandos (separados por ;)
        commands = sql_script.split(';')
        
        for command in commands:
            command = command.strip()
            if command and not command.startswith('--'):
                try:
                    cursor.execute(command)
                    connection.commit()
                except Error as e:
                    # Ignorar erros de comandos vazios ou comentários
                    if 'empty query' not in str(e).lower():
                        print(f"  ⚠ Aviso: {e}")
        
        print(f"✓ Arquivo SQL executado com sucesso")
        cursor.close()
        return True
        
    except Exception as e:
        print(f"✗ Erro ao executar SQL: {e}")
        return False


def verify_data(connection):
    """Verifica os dados carregados"""
    try:
        cursor = connection.cursor(dictionary=True)
        
        print("\n" + "="*80)
        print("VERIFICAÇÃO DOS DADOS CARREGADOS")
        print("="*80)
        
        # Contar registros
        cursor.execute("SELECT COUNT(*) as total FROM car_sales")
        result = cursor.fetchone()
        print(f"\n✓ Total de registros na tabela: {result['total']}")
        
        # Estatísticas básicas
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT car_id) as unique_cars,
                COUNT(DISTINCT customer_name) as unique_customers,
                COUNT(DISTINCT dealer_name) as dealers,
                COUNT(DISTINCT company) as brands,
                COUNT(DISTINCT model) as models,
                MIN(sale_date) as first_date,
                MAX(sale_date) as last_date,
                SUM(price) as total_revenue,
                AVG(price) as avg_price
            FROM car_sales
        """)
        
        stats = cursor.fetchone()
        print(f"\n📊 Estatísticas:")
        print(f"  • Carros únicos: {stats['unique_cars']}")
        print(f"  • Clientes únicos: {stats['unique_customers']}")
        print(f"  • Concessionárias: {stats['dealers']}")
        print(f"  • Marcas: {stats['brands']}")
        print(f"  • Modelos: {stats['models']}")
        print(f"  • Período: {stats['first_date']} a {stats['last_date']}")
        print(f"  • Receita total: ${stats['total_revenue']:,.2f}")
        print(f"  • Preço médio: ${stats['avg_price']:,.2f}")
        
        # Top 5 modelos mais vendidos
        cursor.execute("""
            SELECT company, model, COUNT(*) as sales
            FROM car_sales
            GROUP BY company, model
            ORDER BY sales DESC
            LIMIT 5
        """)
        
        print(f"\n🏆 Top 5 Modelos Mais Vendidos:")
        for row in cursor.fetchall():
            print(f"  • {row['company']} {row['model']}: {row['sales']} vendas")
        
        cursor.close()
        return True
        
    except Error as e:
        print(f"✗ Erro ao verificar dados: {e}")
        return False


def main():
    """Função principal"""
    print("="*80)
    print("PROJETO INTEGRADOR - CARGA DE DADOS")
    print("="*80)
    print(f"Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Conectar ao banco
    connection = create_connection()
    if not connection:
        sys.exit(1)
    
    # 2. Carregar e transformar dados do CSV
    df = load_csv_data(CSV_FILE)
    if df is None:
        connection.close()
        sys.exit(1)
    
    # 3. Inserir dados no banco
    success = insert_data_batch(connection, df)
    if not success:
        connection.close()
        sys.exit(1)
    
    # 4. Executar script DML para popular dimensões
    print("\n→ Populando tabelas dimensionais...")
    execute_sql_file(connection, 'car_sales_dml.sql')
    
    # 5. Verificar dados carregados
    verify_data(connection)
    
    # 6. Fechar conexão
    connection.close()
    print("\n✓ Conexão fechada")
    
    print(f"\nFim: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    print("✓ PROCESSO CONCLUÍDO COM SUCESSO!")
    print("="*80)


if __name__ == "__main__":
    main()
