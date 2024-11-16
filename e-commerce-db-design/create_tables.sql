CREATE DATABASE IF NOT EXISTS E_COMMERCE;

USE E_COMMERCE;

CREATE TABLE IF NOT EXISTS Users (
    UserID INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary key identifier for each user',
    Username VARCHAR(50) NOT NULL COMMENT 'Username chosen by the user',
    Email VARCHAR(100) NOT NULL UNIQUE COMMENT 'User email, must be unique',
    PasswordHash VARCHAR(255) NOT NULL COMMENT 'Hashed password for user authentication',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the user was created'
) COMMENT = 'Stores user account details';

CREATE UNIQUE INDEX idx_users_email ON Users (Email);

CREATE TABLE IF NOT EXISTS UserProfile (
    UserProfileID INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary key for user profile details',
    UserID INT UNIQUE NOT NULL COMMENT 'Foreign key to Users',
    FullName VARCHAR(100) COMMENT 'Full name of the user',
    Address VARCHAR(255) COMMENT 'User address information',
    PhoneNumber VARCHAR(20) COMMENT 'Contact phone number for the user',
    DateOfBirth DATE COMMENT 'Date of birth of the user',
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
) COMMENT = 'Stores additional profile information for each user';

CREATE TABLE IF NOT EXISTS Products (
    ProductID INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary key identifier for each product',
    ProductName VARCHAR(100) NOT NULL COMMENT 'Name of the product',
    Description TEXT COMMENT 'Detailed description of the product',
    Price DECIMAL(10, 2) NOT NULL COMMENT 'Price of the product',
    Stock INT NOT NULL DEFAULT 0 COMMENT 'Current stock level of the product',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the product was added to the catalog'
) COMMENT = 'Contains information about products available in the store';

CREATE INDEX idx_products_productname ON Products (ProductName);

CREATE TABLE IF NOT EXISTS Orders (
    OrderID INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary key identifier for each order',
    UserID INT NOT NULL COMMENT 'Identifier of the user placing the order',
    OrderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp of when the order was placed',
    Status ENUM('Pending', 'Shipped', 'Delivered', 'Cancelled') DEFAULT 'Pending' COMMENT 'Current status of the order',
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
) COMMENT = 'Stores details of each order placed by users';

CREATE INDEX idx_orders_userid ON Orders (UserID);

CREATE TABLE IF NOT EXISTS Order_Products (
    OrderProductID INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary key for the order-product relationship',
    OrderID INT NOT NULL COMMENT 'Identifier of the order',
    ProductID INT NOT NULL COMMENT 'Identifier of the product in the order',
    Quantity INT NOT NULL COMMENT 'Quantity of the product ordered',
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID) ON DELETE CASCADE
) COMMENT = 'Associates products with orders, recording the quantity of each product in an order';

CREATE INDEX idx_order_products_orderid ON Order_Products (OrderID);
CREATE INDEX idx_order_products_productid ON Order_Products (ProductID);
