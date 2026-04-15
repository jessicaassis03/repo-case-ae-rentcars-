-- Query cobrindo as 5 perguntas do negócio
-- Q1: Taxa de conversão por funil (sessão → busca → reserva), segmentada por país e device
-- Lógica: contar sessões, buscas e reservas distintas e calcular proporções
select
    s.country,
    lower(s.device) as device,
    count(distinct s.session_id) as total_sessions,
    count(distinct se.search_id) as total_searches,
    count(distinct b.booking_id) as total_bookings,
    round(count(distinct b.booking_id)::numeric / nullif(count(distinct s.session_id),0), 4) as conversion_rate
from raw_sessions s
left join raw_searches se on s.session_id = se.session_id
left join raw_bookings b on s.session_id = b.session_id
where s.is_bot = false
group by s.country, lower(s.device)
order by conversion_rate desc;

-- Q2: Top 10 parceiros por receita nos últimos 90 dias, excluindo cancelamentos
-- Lógica: somar total_amount apenas para reservas confirmadas ou concluídas
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

-- Q3: LTV (Lifetime Value) dos usuários agrupados por cohort de primeiro acesso (mês/ano)
-- Lógica: identificar primeira reserva do usuário e agrupar por cohort
with first_booking as (
    select
        user_id,
        min(booked_at) as first_access
    from raw_bookings
    where user_id is not null
    group by user_id
),
cohorts as (
    select
        fb.user_id,
        date_trunc('month', fb.first_access) as cohort_month,
        sum(b.total_amount) as ltv
    from first_booking fb
    join raw_bookings b on fb.user_id = b.user_id
    where b.status in ('confirmed','completed')
    group by fb.user_id, cohort_month
)
select cohort_month, avg(ltv) as avg_ltv
from cohorts
group by cohort_month
order by cohort_month;

-- Q4: Detecção de sessões suspeitas de bot — mais de 50 buscas em uma janela de 5 minutos
-- Lógica: contar buscas por sessão em intervalos de 5 minutos
select
    se.session_id,
    count(se.search_id) as num_searches,
    min(se.searched_at) as first_search,
    max(se.searched_at) as last_search
from raw_searches se
group by se.session_id
having count(se.search_id) > 50
   and (max(se.searched_at) - min(se.searched_at)) <= interval '5 minutes';

-- Q5: Taxa de cancelamento por parceiro com identificação de outliers estatísticos (> 2σ)
-- Lógica: calcular taxa de cancelamento e marcar outliers
with cancel_rate as (
    select
        b.partner_id,
        count(c.cancellation_id)::float / nullif(count(b.booking_id),0) as cancellation_rate
    from raw_bookings b
    left join raw_cancellations c on b.booking_id = c.booking_id
    where b.status = 'confirmed'
    group by b.partner_id
),
stats as (
    select
        avg(cancellation_rate) as mean_rate,
        stddev(cancellation_rate) as std_rate
    from cancel_rate
)
select
    p.partner_name,
    cr.cancellation_rate,
    case when cr.cancellation_rate > (s.mean_rate + 2*s.std_rate) then 'outlier' else 'normal' end as flag
from cancel_rate cr
join raw_partners p on cr.partner_id = p.partner_id
cross join stats s
order by cr.cancellation_rate desc;
