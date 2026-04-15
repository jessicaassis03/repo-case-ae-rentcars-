Rentcars Case Técnico
***
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

É um diagrama de relacionamento entre tabelas (ERD simplificado), representando como os dados foram modelados no projeto dbt/marts. Vamos destrinchar:

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
→ Permite calcular taxa de cancelamento, reembolsos e motivos.


O que significa a arquitetura
Dimensões (dim_): tabelas descritivas que enriquecem os fatos (ex.: parceiros, usuários).

Fatos (fct_): tabelas centrais de eventos numéricos (sessões, reservas).

Relacionamentos:

Sessões (fct_sessions) geram buscas e podem resultar em reservas (fct_bookings).

Reservas podem ser canceladas (raw_cancellations).

Reservas e buscas se conectam a parceiros (dim_partners).

Reservas se conectam a usuários (dim_users).

objetivo:
 Essa arquitetura é um star schema simplificado, onde as tabelas de fatos (fct_sessions, fct_bookings) ficam no centro e se relacionam com dimensões (dim_partners, dim_users). Isso facilita análises de receita, conversão, cancelamento e comportamento de usuários de forma consistente e escalável.

****

Decisões Técnicas
Star schema: adotado para clareza e performance em análises.

Incremental models: fct_sessions e fct_bookings com deduplicação por chave (session_id, booking_id).

Normalização de case: todos os campos categóricos convertidos para lower() ou upper().

Deduplicação: distinct aplicado em staging e incremental.


🚨 Limitações Conhecidas
Dados contêm duplicatas e outliers intencionais (fraude, valores negativos).

Não foi implementada anonimização avançada de PII (básico).

O dashboard foi construído em Power BI; exportado em PDF para entrega.

Cohort LTV calculado apenas por mês/ano de primeiro acesso; não há granularidade diária.

🌟 Melhorias Futuras
Implementar Great Expectations para validações adicionais.

Criar pipeline de anonimização para PII (hash + tokenização).

Adicionar alertas automáticos para detecção de fraude em tempo real.

Expandir métricas de funil com atribuição de marketing multicanal.
