
-- ============================================================
-- Main Program 2
-- Order Total & Expired Product Discount Management
--
-- Calls:
-- 1. update_expired_product_discount procedure
-- 2. calculate_order_total function
-- ============================================================

DO $$
DECLARE
    selected_order_id INT := 1;
    order_total_before NUMERIC;
    order_total_after NUMERIC;
    expired_products_count INT;
BEGIN

    RAISE NOTICE '===== MAIN PROGRAM 2 STARTED =====';

    ------------------------------------------------------------
    -- Count products that are close to expiration
    ------------------------------------------------------------
    SELECT COUNT(*)
    INTO expired_products_count
    FROM product
    WHERE expirationdate <= CURRENT_DATE + INTERVAL '30 days';

    RAISE NOTICE
        'Products close to expiration: %',
        expired_products_count;

    ------------------------------------------------------------
    -- Calculate order total before discount procedure
    ------------------------------------------------------------
    SELECT calculate_order_total(selected_order_id)
    INTO order_total_before;

    RAISE NOTICE
        'Order % total before discount procedure: %',
        selected_order_id,
        order_total_before;

    ------------------------------------------------------------
    -- Call procedure: update expired product discounts
    ------------------------------------------------------------
    CALL update_expired_product_discount();

    ------------------------------------------------------------
    -- Calculate order total after discount procedure
    ------------------------------------------------------------
    SELECT SUM(subtotal)
    INTO order_total_after
    FROM orderitem
    WHERE orderid = selected_order_id;

    RAISE NOTICE
        'Order % total according to orderitem after procedure: %',
        selected_order_id,
        order_total_after;

    ------------------------------------------------------------
    -- Compare totals
    ------------------------------------------------------------
    IF order_total_before = order_total_after THEN

        RAISE NOTICE
            'Order total did not change because the discount procedure updates product prices, not orderitem subtotal.';

    ELSE

        RAISE NOTICE
            'Order total changed from % to %.',
            order_total_before,
            order_total_after;

    END IF;

    ------------------------------------------------------------
    -- Final result
    ------------------------------------------------------------
    IF expired_products_count = 0 THEN

        RAISE NOTICE
            'No expired or close-to-expiration products were found.';

    ELSE

        RAISE NOTICE
            'Discount procedure was executed for close-to-expiration products.';

    END IF;

    RAISE NOTICE '===== MAIN PROGRAM 2 FINISHED =====';

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error in Main Program 2: %', SQLERRM;
END $$;