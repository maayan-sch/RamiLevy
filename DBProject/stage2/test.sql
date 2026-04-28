SELECT 
    c.customerid,
    c.customername,
    c.email,
    o.totalamount
FROM customer c
NATURAL JOIN orders o 
WHERE o.totalamount > 200
ORDER BY o.totalamount DESC
LIMIT 100;

SELECT 
    c.customerid,
    c.customername,
    c.email,
    o.totalamount
FROM customer c,
     orders o
WHERE c.customerid = o.customerid
AND o.totalamount > 200
ORDER BY o.totalamount DESC
LIMIT 100;