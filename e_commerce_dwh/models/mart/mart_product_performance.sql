SELECT
    product_id,
    SUM(sale_amount) AS total_revenue,
    COUNT(DISTINCT sales_id) AS total_sales_count
FROM {{ ref('stage_sales_data_cleaned') }}
GROUP BY product_id
