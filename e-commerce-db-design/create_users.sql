USE E_COMMERCE;

CREATE USER 'admin'@'localhost' IDENTIFIED BY 'adminPass';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';

CREATE USER 'manager'@'localhost' IDENTIFIED BY 'managerPass';
GRANT SELECT, INSERT, UPDATE ON ecommerce.* TO 'manager'@'localhost';

CREATE USER 'customer'@'localhost' IDENTIFIED BY 'customerPass';
GRANT SELECT ON ecommerce.Products TO 'customer'@'localhost';