SELECT DISTINCT
    customer_id,
    {{ uppercase('customer_name') }} AS customer_name,
    email
FROM {{ ref('raw_customer_data') }}
WHERE email IS NOT NULL
