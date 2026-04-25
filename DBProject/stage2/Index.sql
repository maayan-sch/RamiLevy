-- Index 1: Check query plan before creating index
EXPLAIN ANALYZE
SELECT orderid, customerid, orderdate, totalamount
FROM orders
WHERE orderdate = '2025-01-01';

-- Create index
CREATE INDEX idx_orders_orderdate ON orders(orderdate);

-- Check again
EXPLAIN ANALYZE
SELECT orderid, customerid, orderdate, totalamount
FROM orders
WHERE orderdate = '2025-01-01';

-- Index 2: Before
EXPLAIN ANALYZE
SELECT *
FROM orders
WHERE customerid = 10;

-- Create index
CREATE INDEX idx_orders_customerid ON orders(customerid);

-- After
EXPLAIN ANALYZE
SELECT *
FROM orders
WHERE customerid = 10;

-- Index 3: Before
EXPLAIN ANALYZE
SELECT *
FROM orderitem
WHERE productid = 5;

-- Create index
CREATE INDEX idx_orderitem_productid ON orderitem(productid);

-- After
EXPLAIN ANALYZE
SELECT *
FROM orderitem
WHERE productid = 5;