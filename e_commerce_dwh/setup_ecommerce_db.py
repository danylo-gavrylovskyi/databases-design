import duckdb

con = duckdb.connect('ecommerce.db')

con.execute("""
CREATE TABLE source_sales_table (
    sales_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    order_id INTEGER,
    sale_date DATE,
    sale_amount DECIMAL
);
""")

con.execute("""
CREATE TABLE source_customer_table (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR,
    email VARCHAR
);
""")

con.execute("""
CREATE TABLE source_product_table (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR,
    category VARCHAR,
    price DECIMAL
);
""")

con.execute("""
CREATE TABLE source_order_table (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE
);
""")

con.execute("""
CREATE TABLE source_transaction_table (
    transaction_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    transaction_amount DECIMAL,
    transaction_date DATE
);
""")

con.execute("""
INSERT INTO source_sales_table (sales_id, customer_id, product_id, order_id, sale_date, sale_amount) VALUES
(1, 1, 1, 1, '2024-01-01', 100.00),
(2, 2, 1, 2, '2024-01-02', 150.50),
(3, 1, 2, 1, '2024-01-03', 200.00);
""")

con.execute("""
INSERT INTO source_customer_table (customer_id, customer_name, email) VALUES
(1, 'John Doe', 'john.doe@example.com'),
(2, 'Jane Smith', 'jane.smith@example.com');
""")

con.execute("""
INSERT INTO source_product_table (product_id, product_name, category, price) VALUES
(1, 'Product A', 'Category 1', 50.00),
(2, 'Product B', 'Category 2', 75.00);
""")

con.execute("""
INSERT INTO source_order_table (order_id, customer_id, order_date) VALUES
(1, 1, '2024-01-01'),
(2, 2, '2024-01-02');
""")

con.execute("""
INSERT INTO source_transaction_table (transaction_id, order_id, transaction_amount, transaction_date) VALUES
(1, 1, 100.00, '2024-01-01'),
(2, 2, 150.50, '2024-01-02');
""")

print("Sales Data:")
print(con.execute("SELECT * FROM source_sales_table").fetchall())

print("\nCustomer Data:")
print(con.execute("SELECT * FROM source_customer_table").fetchall())

print("\nProduct Data:")
print(con.execute("SELECT * FROM source_product_table").fetchall())

print("\nOrder Data:")
print(con.execute("SELECT * FROM source_order_table").fetchall())

print("\nTransaction Data:")
print(con.execute("SELECT * FROM source_transaction_table").fetchall())

con.close()
