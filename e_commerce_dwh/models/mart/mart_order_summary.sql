SELECT
    customer_id,
    COUNT(DISTINCT sales_id) AS total_orders,
    SUM(sale_amount) AS total_order_amount
FROM {{ ref('stage_sales_data_cleaned') }}
GROUP BY customer_id
