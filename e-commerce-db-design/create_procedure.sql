DELIMITER $$

CREATE PROCEDURE CalculateOrderTotal(IN orderId INT, OUT total DECIMAL(10,2))
BEGIN
    SELECT SUM(p.Price * op.Quantity)
    INTO total
    FROM Order_Products op
    JOIN Products p ON op.ProductID = p.ProductID
    WHERE op.OrderID = orderId;
END$$

DELIMITER ;