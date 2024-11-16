USE E_COMMERCE;

CREATE OR REPLACE VIEW OrderDetails AS
EXPLAIN ANALYZE SELECT
    O.OrderID,
    U.Username AS Customer_Username,
    U.Email AS Customer_Email,
    O.OrderDate,
    O.Status,
    P.ProductName AS Product_Name,
    P.Price AS Product_Price,
    OP.Quantity AS Quantity_Ordered,
    (P.Price * OP.Quantity) AS Total_Price
FROM Orders O
JOIN Users U ON O.UserID = U.UserID
JOIN Order_Products OP ON O.OrderID = OP.OrderID
JOIN Products P ON OP.ProductID = P.ProductID
ORDER BY O.OrderDate DESC;