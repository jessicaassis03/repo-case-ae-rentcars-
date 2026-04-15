# repo-case-ae-rentcars-
Data Engineer Analytics

#  Rentcars - Case Técnico | 

##  Visão Geral

Este repositório apresenta a solução completa do case técnico da Rentcars, contemplando:

* Modelagem de dados com dbt
* SQL analítico avançado
* Visualização e storytelling
* Governança e qualidade de dados
* Discovery com stakeholders e data contracts

O objetivo foi construir uma solução **escalável, confiável e orientada ao negócio**, tratando inconsistências intencionais nos dados e gerando insights acionáveis.

---

## 🏗️ Arquitetura

```
RAW (CSV)
  ↓
STAGING (limpeza + padronização)
  ↓
INTERMEDIATE (regras de negócio)
  ↓
MARTS (fatos e dimensões)
  ↓
BI / SQL / Analytics
```

---

##  Tecnologias Utilizadas

* dbt
* SQL (ANSI)
* dbt-expectations
* Python (análise)
* Power BI / Looker Studio (dashboard)

---

##  Como Executar

### Pré-requisitos

* Python 3.10+
* dbt-core
* Adapter (ex: dbt-postgres / dbt-duckdb)

### Instalação

```bash
pip install dbt-core dbt-duckdb
```

### Execução

```bash
dbt seed
dbt run
dbt test
dbt docs generate
dbt docs serve
```

---

##  Modelagem

### Abordagem

Foi adotado **Star Schema**, com:

* `dim_users`
* `dim_partners`
* `fct_sessions`
* `fct_bookings`

### Decisões

* Modelos incrementais para escalabilidade
* Deduplicação por chave única
* Padronização de dados no staging
* Separação clara entre lógica técnica e de negócio

---

##  Qualidade de Dados

### Problemas identificados

* Duplicatas
* Datas futuras inválidas
* Inconsistência de países
* Valores negativos
* Sessões com comportamento de bot
* Cancelamentos sem booking

### Soluções

* Testes dbt (nativos + customizados)
* Validações com dbt-expectations
* Regras de limpeza no staging
* Monitoramento de SLA

---

## Principais Insights

* Taxa de conversão varia significativamente por device
* Parceiros com maior volume apresentam maior taxa de cancelamento
* Existem padrões claros de comportamento automatizado (bots)
* Receita líquida difere significativamente da bruta

---

##  Governança

* Definição de SLA de dados
* Catálogo de métricas
* Identificação e tratamento de PII
* Data contracts para alinhamento com negócio

---

##  Stakeholders

Foi realizada simulação com área de **Revenue/Pricing**, com:

* Levantamento de KPIs
* Mapeamento AS-IS vs TO-BE
* Definição de métricas
* Resolução de conflitos conceituais

---

##  Limitações

* Dados simulados com volume limitado
* Ausência de ingestão em tempo real
* Não implementação de monitoramento automático

---

##  Melhorias Futuras

* Orquestração com Airflow
* Monitoramento com alertas
* Camada de feature store
* Detecção de fraude com ML

---

## 📂 Estrutura

```
dbt/
sql/
dashboard/
stakeholders/
governance.md
README.md
```

---

##  Conclusão

A solução foi construída com foco em:

* Confiabilidade
* Escalabilidade
* Clareza para o negócio
* Boas práticas de engenharia de dados

Este projeto demonstra demonstra habilidades técnicas, mas também **visão analítica e alinhamento com stakeholders** 
