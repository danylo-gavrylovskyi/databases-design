SELECT *
FROM {{ ref('stage_product_details') }}
WHERE price <= 0
