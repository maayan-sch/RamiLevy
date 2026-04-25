--Query 1A: Customers with orders above 200
SELECT 
    c.customerid,
    c.customername,
    c.email,
    o.orderid,
    o.orderdate,
    o.totalamount
FROM customer c
JOIN orders o ON c.customerid = o.customerid
WHERE o.totalamount > 200
ORDER BY o.totalamount DESC;

-- Query 1B: Customers with orders above 200 (using subquery)
SELECT 
    c.customerid,
    c.customername,
    c.email,
    c.phone
FROM customer c
WHERE c.customerid IN (
    SELECT o.customerid
    FROM orders o
    WHERE o.totalamount > 200
)
ORDER BY c.customername;

-- Query 2A: Products with quantity below minimum stock (using JOIN)
SELECT
    p.productid,
    p.productname,
    s.storeid,
    s.storename,
    i.quantity,
    i.minimumstock
FROM product p
JOIN inventory i ON p.productid = i.productid
JOIN store s ON i.storeid = s.storeid
WHERE i.quantity < i.minimumstock
ORDER BY i.quantity ASC;

-- Query 2B: Products with quantity below minimum stock (using EXISTS)
SELECT
    p.productid,
    p.productname,
    p.price,
    p.expirationdate
FROM product p
WHERE EXISTS (
    SELECT 1
    FROM inventory i
    WHERE i.productid = p.productid
      AND i.quantity < i.minimumstock
)
ORDER BY p.productname;

-- Query 3A: Suppliers and their products by category (using JOIN)
SELECT
    s.supplierid,
    s.suppliername,
    s.phone,
    p.productid,
    p.productname,
    c.categoryname
FROM supplier s
JOIN product p ON s.supplierid = p.supplierid
JOIN category c ON p.categoryid = c.categoryid
WHERE c.categoryname = 'Dairy'
ORDER BY s.suppliername;

-- Query 3B: Suppliers that provide products from a specific category (using subquery)
SELECT
    s.supplierid,
    s.suppliername,
    s.phone,
    s.city,
    s.street
FROM supplier s
WHERE s.supplierid IN (
    SELECT p.supplierid
    FROM product p
    JOIN category c ON p.categoryid = c.categoryid
    WHERE c.categoryname = 'Dairy'
)
ORDER BY s.suppliername;

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
ORDER BY o.orderdate;

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
ORDER BY o.orderdate;

-- Query 5: Total sales by category
SELECT
    c.categoryid,
    c.categoryname,
    COUNT(oi.orderitemid) AS total_items_sold,
    SUM(oi.subtotal) AS total_sales
FROM category c
JOIN product p ON c.categoryid = p.categoryid
JOIN orderitem oi ON p.productid = oi.productid
GROUP BY c.categoryid, c.categoryname
ORDER BY total_sales DESC;

-- Query 6: Best selling products
SELECT
    p.productid,
    p.productname,
    c.categoryname,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.subtotal) AS total_revenue
FROM product p
JOIN category c ON p.categoryid = c.categoryid
JOIN orderitem oi ON p.productid = oi.productid
GROUP BY p.productid, p.productname, c.categoryname
ORDER BY total_quantity_sold DESC;

-- Query 7: Expired or soon-to-expire products
SELECT
    p.productid,
    p.productname,
    p.dateofmanufacture,
    p.expirationdate,
    p.price
FROM product p
WHERE p.expirationdate <= CURRENT_DATE + INTERVAL '30 days'
ORDER BY p.expirationdate;

-- Query 8: Store inventory summary
SELECT
    s.storeid,
    s.storename,
    s.rating,
    COUNT(i.productid) AS number_of_products,
    SUM(i.quantity) AS total_inventory_quantity
FROM store s
JOIN inventory i ON s.storeid = i.storeid
GROUP BY s.storeid, s.storename, s.rating
ORDER BY total_inventory_quantity DESC;

-- Update 1: Show products before price update
SELECT productid, productname, price, categoryid
FROM product
WHERE categoryid = 1;

-- Update 1: Increase price by 10% for a specific category
UPDATE product
SET price = price * 1.10
WHERE categoryid = 1;

-- Update 1: Show products after price update
SELECT productid, productname, price, categoryid
FROM product
WHERE categoryid = 1;

-- Update 2: Show orders before status update
SELECT orderid, orderdate, totalamount, orderstatus
FROM orders
WHERE orderstatus = 'Pending';

-- Update 2: Change order status to Delivered
UPDATE orders
SET orderstatus = 'Delivered'
WHERE orderstatus = 'Pending';

-- Update 2: Show orders after status update
SELECT orderid, orderdate, totalamount, orderstatus
FROM orders
WHERE orderstatus = 'Delivered';

-- Update 3: Show stores before rating update
SELECT storeid, storename, rating
FROM store;

-- Update 3: Increase rating for stores with high inventory
UPDATE store
SET rating = rating + 0.5
WHERE storeid IN (
    SELECT i.storeid
    FROM inventory i
    GROUP BY i.storeid
    HAVING SUM(i.quantity) > 500
);

-- Update 3: Show stores after rating update
SELECT storeid, storename, rating
FROM store;

-- Delete 1: Show small order items before delete
SELECT orderid, orderitemid, productid, quantity, subtotal
FROM orderitem
WHERE orderid <= 5;

-- Delete 1: Delete small order items
DELETE FROM orderitem
WHERE orderid <= 5;

-- Delete 1: Show order items after delete
SELECT orderid, orderitemid, productid, quantity, subtotal
FROM orderitem
WHERE orderid <= 5;

-- Delete 2: Show order items with low quantity
SELECT orderid, orderitemid, productid, quantity, subtotal
FROM orderitem
WHERE quantity <= 2;

-- Delete 2: Delete order items with low quantity
DELETE FROM orderitem
WHERE quantity <= 2;

-- Delete 2: Show remaining order items
SELECT orderid, orderitemid, productid, quantity, subtotal
FROM orderitem
WHERE quantity <= 2;

-- Delete 3: Show specific order items
SELECT orderid, orderitemid, productid, quantity, subtotal
FROM orderitem
WHERE orderitemid IN (21,22,23,24,25);

-- Delete 3: Delete those specific order items
DELETE FROM orderitem
WHERE orderitemid IN (21,22,23,24,25);

-- Delete 3: Show after delete
SELECT orderid, orderitemid, productid, quantity, subtotal
FROM orderitem
WHERE orderitemid IN (21,22,23,24,25);