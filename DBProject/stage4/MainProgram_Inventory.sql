-- ============================================================
-- Main Program 1
-- Calls:
-- 1. restock_inventory procedure
-- 2. get_low_stock_products function
-- ============================================================

CALL restock_inventory();

BEGIN;

SELECT get_low_stock_products();

FETCH ALL IN "low_stock_cursor";

COMMIT;


/*SELECT
    storeid,
    productid,
    quantity,
    minimumstock
FROM inventory
WHERE quantity < minimumstock;

CALL restock_inventory();

SELECT
    storeid,
    productid,
    quantity,
    minimumstock
FROM inventory
WHERE quantity < minimumstock;*/