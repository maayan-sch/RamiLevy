-- Rollback example: Show product before update
SELECT productid, productname, price
FROM product
WHERE productid = 10;

BEGIN;

-- Rollback example: Update product price
UPDATE product
SET price = price + 100
WHERE productid = 10;

-- Rollback example: Show product after update
SELECT productid, productname, price
FROM product
WHERE productid = 10;

ROLLBACK;

-- Rollback example: Show product after rollback
SELECT productid, productname, price
FROM product
WHERE productid = 10;

-- Commit example: Show product before update
SELECT productid, productname, price
FROM product
WHERE productid = 11;

BEGIN;

-- Commit example: Update product price
UPDATE product
SET price = price + 50
WHERE productid = 11;

-- Show after update
SELECT productid, productname, price
FROM product
WHERE productid = 11;

COMMIT;

-- Show after commit
SELECT productid, productname, price
FROM product
WHERE productid = 11;