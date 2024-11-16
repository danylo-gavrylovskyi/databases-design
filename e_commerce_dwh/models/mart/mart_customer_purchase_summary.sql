SELECT
    customer_id,
    COUNT(DISTINCT sales_id) AS total_sales_count,
    SUM(sale_amount) AS total_spent
FROM {{ ref('stage_sales_data_cleaned') }}
GROUP BY customer_id
