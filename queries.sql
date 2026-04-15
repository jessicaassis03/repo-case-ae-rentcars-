-- =========================================
-- Q1: Funil de Conversão por país e device
-- =========================================
WITH sessions AS (
    SELECT DISTINCT session_id, country, device
    FROM fct_sessions
),
searches AS (
    SELECT DISTINCT session_id FROM stg_searches
),
bookings AS (
    SELECT DISTINCT session_id FROM fct_bookings
)

SELECT
    s.country,
    s.device,
    COUNT(DISTINCT s.session_id) AS total_sessions,
    COUNT(DISTINCT se.session_id) AS total_searches,
    COUNT(DISTINCT b.session_id) AS total_bookings,
    ROUND(COUNT(DISTINCT b.session_id) * 1.0 / COUNT(DISTINCT s.session_id), 4) AS conversion_rate
FROM sessions s
LEFT JOIN searches se USING(session_id)
LEFT JOIN bookings b USING(session_id)
GROUP BY s.country, s.device
ORDER BY conversion_rate DESC;


-- =========================================
-- Q2: Top 10 parceiros por receita (90 dias)
-- =========================================
SELECT
    partner_id,
    SUM(total_amount) AS revenue
FROM fct_bookings
WHERE created_at >= CURRENT_DATE - INTERVAL '90 days'
  AND is_canceled = 0
GROUP BY partner_id
ORDER BY revenue DESC
LIMIT 10;


-- =========================================
-- Q3: LTV por cohort
-- =========================================
WITH first_touch AS (
    SELECT
        user_id,
        MIN(session_start) AS first_seen
    FROM fct_sessions
    GROUP BY user_id
),

cohort AS (
    SELECT
        user_id,
        DATE_TRUNC('month', first_seen) AS cohort_month
    FROM first_touch
),

ltv AS (
    SELECT
        b.user_id,
        SUM(b.total_amount) AS total_ltv
    FROM fct_bookings b
    WHERE is_canceled = 0
    GROUP BY b.user_id
)

SELECT
    c.cohort_month,
    AVG(l.total_ltv) AS avg_ltv
FROM cohort c
LEFT JOIN ltv l USING(user_id)
GROUP BY c.cohort_month
ORDER BY c.cohort_month;


-- =========================================
-- Q4: Sessões suspeitas de bot
-- =========================================
SELECT
    session_id,
    DATE_TRUNC('minute', search_time) AS minute_window,
    COUNT(*) AS searches
FROM stg_searches
GROUP BY session_id, minute_window
HAVING COUNT(*) > 50
ORDER BY searches DESC;


-- =========================================
-- Q5: Taxa de cancelamento + outliers
-- =========================================
WITH cancel_rate AS (
    SELECT
        partner_id,
        COUNT(*) FILTER (WHERE is_canceled = 1) * 1.0 / COUNT(*) AS cancel_rate
    FROM fct_bookings
    GROUP BY partner_id
),

stats AS (
    SELECT
        AVG(cancel_rate) AS avg_rate,
        STDDEV(cancel_rate) AS stddev_rate
    FROM cancel_rate
)

SELECT
    c.partner_id,
    c.cancel_rate,
    CASE
        WHEN c.cancel_rate > s.avg_rate + 2 * s.stddev_rate THEN 'OUTLIER'
        ELSE 'NORMAL'
    END AS classification
FROM cancel_rate c
CROSS JOIN stats s
ORDER BY c.cancel_rate DESC;
