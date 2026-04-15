-- Modelo staging
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
