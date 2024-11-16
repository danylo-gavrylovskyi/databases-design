SELECT DISTINCT
    sales_id,
    customer_id,
    product_id,
    sale_date,
    sale_amount
FROM {{ ref('raw_sales_data') }}
WHERE sale_amount > 0
