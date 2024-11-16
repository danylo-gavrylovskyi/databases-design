SELECT
    COUNT(DISTINCT sales_id) AS total_sales,
    SUM(sale_amount) AS total_amount
FROM {{ ref('stage_sales_data_cleaned') }}
