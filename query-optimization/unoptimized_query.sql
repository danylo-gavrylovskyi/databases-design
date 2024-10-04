SELECT
    (SELECT COUNT(o.order_id) 
     FROM (SELECT order_id, product_id, client_id 
           FROM opt_orders 
           WHERE order_date BETWEEN '2022-01-01' AND '2023-01-01') AS sub_orders
     JOIN opt_products ON sub_orders.product_id = opt_products.product_id
     WHERE opt_products.product_category = 'Category1') AS category1_order_count,

    (SELECT CONCAT(c.name, " ", c.surname, ": ", total_spent) 
     FROM (SELECT client_id, SUM(p.price) AS total_spent 
           FROM (SELECT o.client_id, o.product_id 
                 FROM opt_orders o 
                 WHERE o.order_date BETWEEN '2021-01-01' AND '2022-01-01') AS sub_orders
           JOIN opt_products p ON sub_orders.product_id = p.product_id
           GROUP BY client_id) AS sub_clients
     JOIN opt_clients c ON sub_clients.client_id = c.id
     ORDER BY total_spent DESC
     LIMIT 1) AS top_spending_client,

    (SELECT AVG(p.price) 
     FROM (SELECT product_id 
           FROM opt_orders 
           WHERE order_date > '2023-01-01') AS recent_orders
     JOIN opt_products p ON recent_orders.product_id = p.product_id
     JOIN opt_clients c ON c.id = (SELECT client_id FROM opt_orders WHERE order_date < '2021-01-01' LIMIT 1)) AS avg_price_recent_orders,

    (SELECT COUNT(DISTINCT o.client_id) 
     FROM opt_orders o
     JOIN opt_clients c ON o.client_id = c.id
     WHERE o.order_date BETWEEN '2020-01-01' AND '2021-01-01'
     AND c.status = 'active') AS distinct_active_clients;
