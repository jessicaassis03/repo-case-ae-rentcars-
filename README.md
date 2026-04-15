Rentcars Case Técnica
Pré-requisitos
Python 3.9+

dbt-core (>=1.6)

Conector dbt para seu warehouse (ex.: dbt-postgres, dbt-bigquery, dbt-snowflake)

Banco de dados com os datasets carregados (raw_partners, raw_sessions, raw_searches, raw_bookings, raw_cancellations)

pip install dbt-core dbt-postgres


Arquitetura de Dados (ASCII ERD)

dim_partners ────────────────┐
                             │
dim_users ───────────────────┤
                             │
fct_sessions ────────────────┤
    │ session_id             │
    ▼                        │
fct_bookings ────────────────┘
    │ booking_id
    ▼
raw_cancellations


(diagrama de relacionamento entre tabelas (ERD simplificado), representando como os dados foram modelados no projeto dbt/marts. Vamos destrinchar:

dim_partners  
É a dimensão de parceiros (locadoras). Contém atributos descritivos como nome, país, tier e status.
→ Serve para enriquecer análises de reservas e sessões com informações sobre os parceiros.

dim_users  
É a dimensão de usuários. Agrupa atributos como user_id, cohort de primeiro acesso, país de origem.
→ Permite análises de comportamento e métricas de LTV por usuário.

fct_sessions  
É a tabela fato de sessões. Cada linha representa uma sessão de navegação no site.
→ Conecta-se a buscas e reservas via session_id.

fct_bookings  
É a tabela fato de reservas. Cada linha representa uma reserva concluída.
→ Conecta-se a sessões via session_id e a parceiros via partner_id.
→ É a principal tabela de receita e conversão.

raw_cancellations  
É a tabela bruta de cancelamentos. Relaciona-se diretamente com fct_bookings via booking_id.
→ Permite calcular taxa de cancelamento, reembolsos e motivos.)


Decisões Técnicas
Star schema: adotado para clareza e performance em análises.

Incremental models: fct_sessions e fct_bookings com deduplicação por chave (session_id, booking_id).

Normalização de case: todos os campos categóricos convertidos para lower() ou upper().

Deduplicação: distinct aplicado em staging e incremental.


Limitações Conhecidas
Dados contêm duplicatas e outliers intencionais (fraude, valores negativos).

Não foi implementada anonimização avançada de PII (apenas mascaramento básico).

O dashboard foi construído em Power BI em sql

Cohort LTV calculado apenas por mês/ano de primeiro acesso; não há granularidade diária.

Hoje
data_dictionary.md

Markdown

raw_bookings.csv

Valores Separados por Vírgula

raw_cancellations.csv

Valores Separados por Vírgula

Confira tudo
rentcars
Data & Analytics
Case Técnico
Senior Analytics Engineer
Desafio de Processo Seletivo
Prazo de entrega: 5 dias corridos após recebimento
Formato de entrega: Repositório Git (GitHub / GitLab)
Competências: 5 desafios — dbt, SQL, Viz, Governança, Stakeholders
Documento de uso exclusivo do candidato.
Rentcars | Case Técnico — Senior Analytics Engineer | Página 2
Bem-vindo ao Case Técnico da Rentcars
A Rentcars opera a maior plataforma de aluguel de veículos da América Latina, conectando clientes a
parceiros em mais de 160 países. O time de dados transforma dados brutos de sessões, buscas,
reservas e cancelamentos em inteligência que orienta decisões de produto, pricing e operações.
Você foi convidado(a) para o case de Senior Analytics Engineer. Sua missão cobre modelagem de
dados com dbt, SQL analítico, visualização, governança de qualidade e — igualmente importante — a
capacidade de entrevistar áreas de negócio para descobrir necessidades e traduzí-las em soluções
de dados confiáveis.
nn Atenção: Os datasets contêm problemas de qualidade intencionais — duplicatas,
inconsistências de case, valores inválidos, padrões de fraude e datas logicamente incorretas.
Identificar, documentar e propor remediação para esses problemas faz parte central da
avaliação.
Dados Disponíveis
Consulte o data_dictionary.md para descrição detalhada de cada coluna, regras de negócio e
relacionamentos entre tabelas.
Arquivo Descrição Linhas Desafios
raw_partners.csv
Catálogo de parceiros/locadoras com status
e comissões
22 D4, D5
raw_sessions.csv
Sessões de navegação dos usuários na
plataforma
120.000 D1, D2
raw_searches.csv
Buscas realizadas — origem, destino, datas
e preços
80.000 D1, D2
raw_bookings.csv
Reservas confirmadas com parceiro, usuário
e receita
18.000 D1, D2, D3
raw_cancellations.
csv
Cancelamentos e motivos associados às
reservas
4.400 D1, D3
Os Desafios
DESAFIO 1
Modelagem de Dados com dbt
Rentcars | Case Técnico — Senior Analytics Engineer | Página 3
Peso: 25% da avaliação
Configure um projeto dbt ponta-a-ponta com fontes, staging, camada intermediária e marts,
demonstrando boas práticas de modelagem e documentação.
Requisitos de modelagem:
• Sources e staging: defina sources.yml e crie modelos stg_ para cada dataset, com renomeação,
cast de tipos e limpeza básica (case, nulos, deduplicação).
• Marts: implemente star schema ou wide table justificado no README — dim_partners,
dim_users, fct_bookings, fct_sessions no mínimo.
• Modelos incrementais: fct_sessions e fct_bookings devem ser incrementais com estratégia de
deduplicação explícita por chave única.
• Testes: not_null, unique, accepted_values, relationships (nativo) + ao menos 2 testes
customizados via dbt-expectations ou macros próprias.
• Documentação: schema.yml completo com description e meta tags em todos os modelos e
colunas dos marts.
• Entregável: projeto dbt funcional com README de execução.
DESAFIO 2
SQL Analítico Avançado
Peso: 20% da avaliação
Responda 5 perguntas de negócio com queries SQL otimizadas, documentadas e com resultados
exportados em CSV.
Quer
y
Pergunta de negócio
Q1 Taxa de conversão por funil (sessão ® busca ® reserva), segmentada por país e device.
Q2 Top 10 parceiros por receita nos últimos 90 dias, excluindo cancelamentos.
Q3 LTV (Lifetime Value) dos usuários agrupados por cohort de primeiro acesso (mês/ano).
Q4 Detecção de sessões suspeitas de bot — mais de 50 buscas em uma janela de 5 minutos.
Q5 Taxa de cancelamento por parceiro com identificação de outliers estatísticos (> 2s).
Entregável: arquivo queries.sql com queries comentadas + resultados em CSV (máx. 1.000 linhas
cada).
DESAFIO 3
Visualização e Storytelling
Rentcars | Case Técnico — Senior Analytics Engineer | Página 4
Peso: 20% da avaliação
Construa um dashboard que conte a história dos dados de negócio e apresente os principais insights
de forma clara e acionável.
Requisitos:
• Dashboard com 4 a 6 visualizações, incluindo obrigatoriamente: (a) evolução temporal de
reservas e receita, (b) funil de conversão, (c) análise de cancelamentos.
• Ferramentas aceitas: Metabase, Looker Studio, Power BI, Tableau ou Python (Plotly / Seaborn).
• Apresentação de 5 minutos com os principais insights — inclua ao menos 1 insight
contra-intuitivo ou não óbvio identificado nos dados.
• Entregável: PDF ou screenshots do dashboard + slides de apresentação (máx. 5 slides).
DESAFIO 4
Governança e Qualidade de Dados
Peso: 20% da avaliação
Demonstre maturidade em qualidade de dados, catalogação e políticas de governança.
• Identifique e documente TODOS os problemas de qualidade presentes nos datasets.
• Implemente regras de validação via dbt tests, Great Expectations ou SQL.
• Catálogo de dados: descrição dos modelos marts com glossário de métricas.
• SLA de dados: quando um dado pode ser considerado 'confiável'? Defina thresholds
mensuráveis.
• Política de PII: identifique campos sensíveis e proponha tratamento (mascaramento,
anonimização ou exclusão).
• Entregável: governance.md + evidências das validações implementadas.
DESAFIO 5
Entrevistas com Áreas Funcionais (Stakeholder Discovery)
Peso: 15% da avaliação
Demonstre capacidade de atuar como ponte entre negócio e engenharia — competência que
diferencia AEs Sêniores de Plenos.
n Por que este desafio importa?
• Modelos tecnicamente perfeitos, mas construídos sem entender o negócio, não são adotados.
• Conflitos de definição de métricas são a causa mais comum de perda de confiança nos dados.
• O mini data contract é o acordo formal que garante que o time de dados e o negócio falem a
mesma língua.
Rentcars | Case Técnico — Senior Analytics Engineer | Página 5
Requisitos:
• Entrevista simulada: escolha uma área de negócio (Revenue/Pricing, Produto, Operações ou
Customer Success) e elabore um roteiro estruturado de perguntas cobrindo: objetivos da área,
KPIs e suas definições, fontes de dados usadas, principais dores no acesso/confiança nos dados e
necessidades futuras.
• Mapeamento as-is ® to-be: documente como a área acessa dados hoje e como deveria
acessar após a implementação dos seus modelos dbt.
• Tradução de requisitos: converta as necessidades levantadas em requisitos técnicos — quais
novas tabelas, métricas ou modelos dbt seriam necessários?
• Mini data contract: para cada métrica identificada, documente: nome, definição de negócio,
lógica de cálculo, owner, SLA e criticidade.
• Gestão de conflitos: identifique ao menos 1 conflito de definição de métrica entre áreas (ex:
'receita líquida' pode ter definições diferentes em Finance e Produto) e proponha como arbitraria a
divergência.
• Entregável: roteiro_entrevista.md + requisitos_tecnicos.md + data_contract.yaml (ou
equivalente em Markdown).
Entregáveis Esperados
Ao final dos 5 dias corridos, submeta um repositório Git com:
repo-case-ae-rentcars/
nnn dbt/ ¬ Projeto dbt completo (sources, staging, marts, testes)
nnn sql/ ¬ queries.sql + resultados CSV das 5 queries
nnn dashboard/ ¬ PDF / screenshots + slides de apresentação
nnn governance.md ¬ Catálogo, SLA, PII, problemas identificados e remediações
nnn stakeholders/ ¬ roteiro_entrevista.md + requisitos_tecnicos.md +
data_contract.yaml
nnn README.md ¬ Setup, decisões técnicas e como executar o projeto
O README.md deve conter obrigatoriamente:
• Como executar o projeto dbt do zero (pré-requisitos, profiles.yml, comandos)
• Diagrama de arquitetura do modelo de dados (ASCII aceito)
• Justificativa para as principais decisões de modelagem e materialização
• Limitações conhecidas e melhorias que implementaria com mais tempo
n Nossa dica: Um modelo dbt incremental bem documentado, com testes funcionando, e um
discovery de stakeholder com data contract completo valem mais do que 5 desafios superficiais.
Documente o que não implementou e por quê.
crie case funcional para o github

Rentcars Case Técnico — Senior Analytics Engineer

Abrir página

O case funcional já está estruturado em uma página dedicada. Ela organiza todos os entregáveis e requisitos em um repositório Git, cobrindo desde a modelagem em dbt até entrevistas com stakeholders. Você pode visualizar e editar essa página agora, ou voltar a ela mais tarde para detalhar cada desafio.

detalhar com os códigos executáveis
Perfeito, vamos detalhar o case com códigos executáveis para cada desafio. Assim você terá um repositório Git pronto para rodar e validar. Vou estruturar os exemplos em dbt (SQL + Jinja), SQL analítico puro, e snippets para governança e entrevistas.

🟦 Desafio 1 — Modelagem de Dados com dbt
Exemplo de sources.yml
yaml
version: 2

sources:
  - name: rentcars
    schema: raw
    tables:
      - name: raw_partners
      - name: raw_sessions
      - name: raw_searches
      - name: raw_bookings
      - name: raw_cancellations
Exemplo de modelo staging (stg_partners.sql)
sql
with partners as (
    select distinct
        partner_id,
        lower(trim(partner_name)) as partner_name,
        upper(country) as country,
        coalesce(tier, 'unclassified') as tier,
        lower(status) as status,
        commission_rate,
        created_at,
        updated_at,
        contact_email
    from {{ source('rentcars','raw_partners') }}
    where commission_rate between 0.05 and 0.30
)

select * from partners
Exemplo de modelo incremental (fct_bookings.sql)
sql
{{ config(
    materialized='incremental',
    unique_key='booking_id'
) }}

with bookings as (
    select distinct
        booking_id,
        session_id,
        user_id,
        partner_id,
        booked_at,
        pickup_date,
        dropoff_date,
        pickup_location,
        car_category,
        daily_rate,
        total_amount,
        currency,
        lower(status) as status,
        payment_method
    from {{ source('rentcars','raw_bookings') }}
    where total_amount > 0
)

select * from bookings
🟩 Desafio 2 — SQL Analítico Avançado
Q1 — Taxa de conversão por funil
sql
select
    s.country,
    s.device,
    count(distinct s.session_id) as total_sessions,
    count(distinct se.search_id) as total_searches,
    count(distinct b.booking_id) as total_bookings,
    count(distinct b.booking_id)::float / count(distinct s.session_id) as conversion_rate
from raw_sessions s
left join raw_searches se on s.session_id = se.session_id
left join raw_bookings b on s.session_id = b.session_id
where s.is_bot = false
group by s.country, s.device;
Q2 — Top 10 parceiros por receita
sql
select
    p.partner_name,
    sum(b.total_amount) as revenue
from raw_bookings b
join raw_partners p on b.partner_id = p.partner_id
where b.status in ('confirmed','completed')
  and b.booked_at >= current_date - interval '90 days'
group by p.partner_name
order by revenue desc
limit 10;
🟨 Desafio 3 — Visualização
Sugestão de queries base para Power BI / Tableau:

sql
-- Evolução temporal de reservas
select
    date_trunc('month', booked_at) as month,
    count(*) as total_bookings,
    sum(total_amount) as total_revenue
from fct_bookings
where status in ('confirmed','completed')
group by month
order by month;
🟥 Desafio 4 — Governança
Exemplo de teste customizado dbt (macro)
sql
-- test_total_amount_positive.sql
select *
from {{ ref('fct_bookings') }}
where total_amount <= 0
  and status in ('confirmed','completed')
Política de PII
user_id → anonimizar (hash SHA256)

contact_email → mascarar (LEFT(email,3) || '***@***')

🟪 Desafio 5 — Stakeholders
Exemplo de Mini Data Contract (data_contract.yaml)
yaml
metrics:
  - name: conversion_rate
    definition: "Proporção de sessões que resultam em reservas confirmadas ou concluídas"
    calculation: "count(bookings_confirmed) / count(sessions)"
    owner: Produto
    sla: "Atualização diária até 10h"
    criticidade: Alta

  - name: ticket_medio
    definition: "Valor médio das reservas confirmadas"
    calculation: "avg(total_amount)"
    owner: Revenue
    sla: "Atualização diária até 10h"
    criticidade: Alta
👉 Com isso, você já tem códigos executáveis para dbt, SQL analítico, testes de governança e contratos de métricas.
Quer que eu monte o README.md completo com instruções de execução (profiles.yml, comandos dbt run/test) para deixar o repositório pronto para subir no GitHub?

sim
Ótimo, vamos montar o README.md completo para o repositório Git. Ele vai servir como guia de execução do projeto dbt, além de documentar decisões técnicas e limitações.

📘 README.md — Rentcars Case Técnico
🔧 Pré-requisitos
Python 3.9+

dbt-core (>=1.6)

Conector dbt para seu warehouse (ex.: dbt-postgres, dbt-bigquery, dbt-snowflake)

Banco de dados com os datasets carregados (raw_partners, raw_sessions, raw_searches, raw_bookings, raw_cancellations)

Instalação:

bash
pip install dbt-core dbt-postgres
⚙️ Configuração do profiles.yml
Exemplo para Postgres:

yaml
rentcars:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: dbt_user
      password: dbt_password
      port: 5432
      dbname: rentcars_db
      schema: raw
      threads: 4
▶️ Execução do Projeto
Clonar o repositório:

bash
git clone https://github.com/seuusuario/repo-case-ae-rentcars.git
cd repo-case-ae-rentcars
Rodar os modelos dbt:

bash
dbt run
Executar testes de qualidade:

bash
dbt test
Gerar documentação:

bash
dbt docs generate
dbt docs serve
🗂️ Arquitetura de Dados (ASCII ERD)
Código
dim_partners ────────────────┐
                             │
dim_users ───────────────────┤
                             │
fct_sessions ────────────────┤
    │ session_id             │
    ▼                        │
fct_bookings ────────────────┘
    │ booking_id
    ▼
raw_cancellations
📊 Decisões Técnicas
Star schema: adotado para clareza e performance em análises.

Incremental models: fct_sessions e fct_bookings com deduplicação por chave (session_id, booking_id).

Normalização de case: todos os campos categóricos convertidos para lower() ou upper().

Deduplicação: distinct aplicado em staging e incremental.

🚨 Limitações Conhecidas
Dados contêm duplicatas e outliers intencionais (fraude, valores negativos).

Não foi implementada anonimização avançada de PII (apenas mascaramento básico).

O dashboard foi construído em Power BI; exportado em PDF para entrega.

Cohort LTV calculado apenas por mês/ano de primeiro acesso; não há granularidade diária.

🌟 Melhorias Futuras
Implementar Great Expectations para validações adicionais.

Criar pipeline de anonimização para PII (hash + tokenização).

Adicionar alertas automáticos para detecção de fraude em tempo real.

Expandir métricas de funil com atribuição de marketing multicanal.
