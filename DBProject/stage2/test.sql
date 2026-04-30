-- Query 4A: Orders in a specific date (using EXTRACT)
SELECT
    c.customerid,
    c.customername,
    o.orderid,
    o.orderdate,
    o.totalamount
FROM customer c
JOIN orders o ON c.customerid = o.customerid
WHERE EXTRACT(DAY FROM o.orderdate) = 1
  AND EXTRACT(MONTH FROM o.orderdate) = 1
  AND EXTRACT(YEAR FROM o.orderdate) = 2025
ORDER BY o.orderdate
LIMIT 100;

-- Query 4B: Orders in a specific month (using BETWEEN)
SELECT
    c.customerid,
    c.customername,
    o.orderid,
    o.orderdate,
    o.totalamount
FROM customer c
JOIN orders o ON c.customerid = o.customerid
WHERE o.orderdate BETWEEN '2025-01-01' AND '2025-01-31'
ORDER BY o.orderdate
LIMIT 100;