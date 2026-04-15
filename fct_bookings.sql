-- Modelo Incremental
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
