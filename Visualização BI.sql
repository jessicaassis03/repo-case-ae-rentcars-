-- Evolução temporal de reservas
select
    date_trunc('month', booked_at) as month,
    count(*) as total_bookings,
    sum(total_amount) as total_revenue
from fct_bookings
where status in ('confirmed','completed')
group by month
order by month;
