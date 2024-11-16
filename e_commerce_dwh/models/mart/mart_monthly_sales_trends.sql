SELECT
    DATE_TRUNC('month', sale_date) AS month,
    SUM(sale_amount) AS monthly_total_sales,
    COUNT(DISTINCT sales_id) AS monthly_total_orders
FROM {{ ref('stage_sales_data_cleaned') }}
GROUP BY month
ORDER BY month
