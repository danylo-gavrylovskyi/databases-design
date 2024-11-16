DELIMITER $$

CREATE TRIGGER UpdateStock AFTER INSERT ON Order_Products
FOR EACH ROW
BEGIN
    UPDATE Products
    SET Stock = Stock - NEW.Quantity
    WHERE ProductID = NEW.ProductID;
END$$

DELIMITER ;