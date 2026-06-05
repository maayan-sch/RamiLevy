-- ============================================================
-- Main Program 2
-- Calls:
-- 1. update_expired_product_discount procedure
-- 2. calculate_order_total function
-- ============================================================

CALL update_expired_product_discount();

SELECT calculate_order_total(1);

/*SELECT orderid, SUM(subtotal)
FROM orderitem
WHERE orderid = 1
GROUP BY orderid;*/