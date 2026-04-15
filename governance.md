
Catálogo de Métricas

Métrica	Definição	Lógica de Cálculo	Owner	SLA	Criticidade

Taxa de Conversão	Proporção de sessões que resultam em reservas confirmadas ou concluídas	count(bookings_confirmed) / count(sessions)	Produto	Diário 10h	Alta
Ticket Médio	Valor médio das reservas confirmadas	avg(total_amount)	Revenue	Diário 10h	Alta
Taxa de Cancelamento	% de reservas canceladas sobre o total de confirmadas	count(cancelled_bookings) / count(confirmed_bookings)	Operações	Diário 10h	Média
LTV (Lifetime Value)	Receita acumulada por usuário desde o primeiro acesso	sum(total_amount) agrupado por user_id	Customer Success	Mensal	Alta
Receita por Parceiro	Receita total atribuída a cada parceiro ativo	sum(total_amount) filtrado por partner_id	Revenue	Diário 10h	Alta

⏱️ SLA de Dados
Sessões (raw_sessions): confiável após 1h do encerramento da sessão.

Buscas (raw_searches): confiável em tempo real, mas sujeito a deduplicação.

Reservas (raw_bookings): confiável após 15 min da confirmação de pagamento.

Cancelamentos (raw_cancellations): confiável após 30 min do evento.

Parceiros (raw_partners): confiável após atualização manual; SLA de 24h.

- Política de PII
Campos sensíveis identificados:

user_id → anonimização via hash SHA256

contact_email → mascaramento (LEFT(email,3) || '***@***')

payment_method → pseudonimização (mapa interno de códigos)

session_id → manter como UUID, mas não expor em dashboards públicos

Tratamento:

Anonimização: irreversível (hash)

Mascaramento: ocultar parte do valor

Pseudonimização: substituir por código interno

🚨 Problemas de Qualidade Identificados
#	Tabela	Tipo de Problema	Descrição
1	Todas	Duplicatas	Registros idênticos inseridos propositalmente
2	raw_sessions	Inconsistência de case	device: desktop / DESKTOP / Mobile ;
3	raw_sessions	Outlier temporal	Sessões > 24h ;
4	raw_searches	Bot/fraude	65 buscas em < 4 min ;
5	raw_searches	Anomalia lógica	dropoff_date < pickup_date ;
6	raw_bookings	Outlier de valor	total_amount negativo, zerado ou > R$15.000 ;
7	raw_bookings	Fraude potencial	1 user_id com 4 reservas no mesmo dia ;
8	raw_partners	Duplicatas	Parceiros repetidos ;
9	raw_partners	Inconsistência de case	status: active / ACTIVE / Active ;
10	raw_cancellations	Outlier temporal	days_before_pickup negativo.

✅ Regras de Validação Implementadas
dbt tests nativos:

unique em booking_id, session_id, partner_id

not_null em chaves primárias

accepted_values em status, device, country

relationships entre tabelas (partner_id, booking_id)

Testes customizados:

total_amount > 0 para reservas confirmadas/concluídas

dropoff_date >= pickup_date em buscas e reservas

commission_rate entre 0.05 e 0.30

👉 Com isso, o governance.md cobre catálogo de métricas, SLA, PII e qualidade de dados.
