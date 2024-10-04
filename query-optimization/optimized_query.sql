WITH orders_after_2020_cte AS (
	SELECT order_id, order_date, client_id, product_id
    FROM opt_orders
    WHERE order_date > '2020-01-01'
),

product_id_and_category_cte AS (
	SELECT product_id, product_category 
    FROM opt_products
),

order_count_cte AS (
	SELECT product_category, status, COUNT(order_id) AS order_count
	FROM orders_after_2020_cte
    JOIN opt_clients c ON orders_after_2020_cte.client_id = c.id
    JOIN product_id_and_category_cte p ON orders_after_2020_cte.product_id = p.product_id
    GROUP BY product_category
)

SELECT 
	(SELECT order_count FROM order_count_cte WHERE product_category = 'Category1' AND status = 'active') AS category1_active_orders,
	(SELECT order_count FROM order_count_cte WHERE product_category = 'Category2' AND status = 'active') AS category2_active_orders,
	(SELECT order_count FROM order_count_cte WHERE product_category = 'Category3' AND status = 'active') AS category3_active_orders,
	
	(SELECT CONCAT(c.name, ' ', c.surname)
	 FROM orders_after_2020_cte
	 JOIN opt_clients c 
	 ORDER BY order_date DESC
	 LIMIT 1) AS most_recent_client,
	
	(SELECT COUNT(DISTINCT client_id)
	 FROM opt_orders o
	 JOIN opt_clients c ON o.client_id = c.id
	 WHERE order_date < '2021-01-01') AS clients_before_2021,
	
	(SELECT order_count FROM order_count_cte WHERE product_category = 'Category5' AND status = 'inactive') AS category5_inactive_orders;