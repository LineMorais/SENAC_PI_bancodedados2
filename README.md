# 📊 Projeto Integrador - Apoio Decisório aos Negócios

**Base de dados:** [Car Sales Report - Kaggle](https://www.kaggle.com/datasets/missionjee/car-sales-report)

---

## 🚗 Vendas e Desempenho Comercial

### Perguntas de negócio

* **Quais são os modelos e marcas mais vendidos no período analisado?**

  ```python
  df_maisvendidos = Agrupar por Data e Empresa(marcas), modelo
  ```

* **Qual é o ticket médio das vendas por região ou concessionária?**

  ```python
  df_ticket_medio = Agrupar por região de revendedor o preço $
  ```

* **Existe sazonalidade nas vendas ao longo do tempo?**

---

### KPIs sugeridos

* **Volume de vendas (número de carros vendidos)**

  ```python
  df_total = contagem dos ID do carro
  ```

* **Receita total e ticket médio de venda**

  ```python
  df_receita_total = Soma da coluna Preço $
  df_media_receita_ano = Média da coluna Preço $
  ```

* **Taxa de crescimento das vendas por mês/trimestre**

---

## 👥 5.2. Perfil do Cliente

### Perguntas de negócio

* **Clientes de maior renda compram quais tipos de veículos?**

  ```python
  df_renda_x_modelo = Fazer faixa de renda do comprador (Renda anual), agrupar por modelo
  ```

* **Existe diferença de preferência entre homens e mulheres?**

  ```python
  df_genero = Porcentagem que tem de homens e mulheres na coluna genero (Gênero / df_total)
  ```

* **Qual é a faixa de renda predominante dos compradores em cada região?**

  ```python
  df_agrupar_faixa_renda = ...
  ```

---

### KPIs sugeridos

* Distribuição de clientes por faixa de renda
* Percentual de vendas por gênero
* Índice de esforço financeiro (preço do carro ÷ renda anual)

---

## 🌍 5.3. Análise Regional

### Perguntas de negócio

* Quais regiões apresentam maior volume de vendas?
* Há diferenças significativas no preço médio entre regiões?
* Quais concessionárias têm melhor desempenho de receita?

---

### KPIs sugeridos

* Receita total por região
* Ticket médio por concessionária
* Ranking de concessionárias por volume de vendas

---

## 📈 5.4. Suporte a Estratégias de Marketing e Expansão

### Perguntas de negócio

* Em quais regiões vale a pena expandir a rede de concessionárias?
* Quais perfis de cliente devem ser priorizados em campanhas de marketing?
* Existe correlação entre perfil socioeconômico e características do veículo adquirido?

---

### KPIs sugeridos

* Taxa de penetração de mercado (vendas ÷ potencial de clientes)
* Segmentação de clientes por perfil (*clusterização*)
* ROI estimado de campanhas regionais
