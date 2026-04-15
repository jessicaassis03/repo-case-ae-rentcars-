-- Q1 — Taxa de conversão por funil
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
