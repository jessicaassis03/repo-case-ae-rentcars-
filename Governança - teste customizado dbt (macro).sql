-- test_total_amount_positive.sql
select *
from {{ ref('fct_bookings') }}
where total_amount <= 0
  and status in ('confirmed','completed')

Política de PII
user_id → anonimizar (hash SHA256)

contact_email → mascarar (LEFT(email,3) || '***@***')
