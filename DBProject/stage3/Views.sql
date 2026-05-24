-- =====================================================
-- Views.sql
-- Views and queries for Stage 3
-- =====================================================


-- =====================================================
-- View 1: Original system perspective
-- Shows customer orders and payment details
-- =====================================================

CREATE OR REPLACE VIEW v_CustomerOrders AS
SELECT 
    c.customerID,
    c.CustomerName,
    o.orderID,
    o.orderDate,
    o.PaymentMethod,
    o.totalAmount
FROM Customer c
JOIN Orders o
ON c.customerID = o.customerID;


-- Show 10 rows from the view
SELECT *
FROM v_CustomerOrders
LIMIT 10;


-- Query 1: Orders paid by credit card
SELECT 
    CustomerName,
    orderID,
    totalAmount
FROM v_CustomerOrders
WHERE PaymentMethod = 'Credit Card'
LIMIT 10;


-- Query 2: Total amount spent by each customer
SELECT 
    CustomerName,
    SUM(totalAmount) AS TotalSpent
FROM v_CustomerOrders
GROUP BY CustomerName
ORDER BY TotalSpent DESC
LIMIT 10;


-- =====================================================
-- View 2: Received system perspective
-- Shows store inventory and product stock levels
-- =====================================================

CREATE OR REPLACE VIEW v_StoreInventory AS
SELECT 
    s.storeID,
    s.StoreName,
    p.productID,
    p.ProductName,
    i.Quantity,
    i.MinimumStock
FROM Store s
JOIN Inventory i
ON s.storeID = i.storeID
JOIN Product p
ON i.productID = p.productID;


-- Show 10 rows from the view
SELECT *
FROM v_StoreInventory
LIMIT 10;


-- Query 1: Products that need restocking
SELECT 
    StoreName,
    ProductName,
    Quantity,
    MinimumStock
FROM v_StoreInventory
WHERE Quantity <= MinimumStock
LIMIT 10;


-- Query 2: Total inventory quantity per store
SELECT 
    StoreName,
    SUM(Quantity) AS TotalItemsInStore
FROM v_StoreInventory
GROUP BY StoreName
LIMIT 10;