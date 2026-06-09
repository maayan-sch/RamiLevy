-- ============================================================
-- Main Program 1

-- ============================================================
DO $$
DECLARE
    low_stock_count_before INT;
    low_stock_count_after INT;
    rec RECORD;
    notification_count INT := 0;
BEGIN

    SELECT COUNT(*)
    INTO low_stock_count_before
    FROM inventory
    WHERE quantity < minimumstock;

    RAISE NOTICE
        'Low stock products before restock: %',
        low_stock_count_before;

    CALL low_stock_products();

    CALL restock_inventory();

    SELECT COUNT(*)
    INTO low_stock_count_after
    FROM inventory
    WHERE quantity < minimumstock;

    RAISE NOTICE
        'Low stock products after restock: %',
        low_stock_count_after;

    IF low_stock_count_after = 0 THEN
        RAISE NOTICE
            'All products were successfully restocked.';
    ELSE
        RAISE NOTICE
            '% products are still below minimum stock.',
            low_stock_count_after;
    END IF;

    RAISE NOTICE
        '===== EXPIRING PRODUCTS SUPPLIER ALERT =====';

    FOR rec IN
        SELECT
            p.productid,
            p.productname,
            p.expirationdate,
            s.suppliername,
            s.email
        FROM product p
        JOIN supplier s
            ON p.supplierid = s.supplierid
        WHERE p.expirationdate <= CURRENT_DATE + INTERVAL '30 days'
    LOOP

        notification_count := notification_count + 1;

        RAISE NOTICE
            'Supplier: %, Product: %, Expiration Date: %',
            rec.suppliername,
            rec.productname,
            rec.expirationdate;

    END LOOP;

    RAISE NOTICE
        'Total supplier notifications sent: %',
        notification_count;

END $$; 

COMMIT

Query returned successfully in 320 msec.

SELECT
    productid,
    quantity,
    minimumstock
FROM inventory
WHERE quantity < minimumstock;