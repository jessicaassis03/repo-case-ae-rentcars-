-- Q2 — Top 10 parceiros por receita
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
