SELECT DISTINCT
    product_id,
    product_name,
    LOWER(category) AS category,
    price
FROM {{ ref('raw_product_data') }}
WHERE price > 0
