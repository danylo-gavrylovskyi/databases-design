WITH order_data AS (
    SELECT 
        o.order_id,
        o.customer_id,
        o.order_date,
        COUNT(s.sales_id) AS items_sold
    FROM 
        {{ ref('raw_order_data') }} o
    LEFT JOIN 
        {{ ref('raw_sales_data') }} s ON o.order_id = s.order_id
    GROUP BY 
        o.order_id, o.customer_id, o.order_date
)

SELECT * FROM order_data
