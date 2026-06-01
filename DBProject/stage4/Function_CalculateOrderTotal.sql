-- =========================================================
-- Function: calculate_order_total
-- Description:
-- This function calculates the total price of a specific order.
-- It goes through all items in the orderitem table using a loop,
-- sums the subtotal values, and returns the final total amount.
--
-- Programming elements used:
-- * Function
-- * FOR LOOP
-- * RECORD
-- * Variables
-- * RETURN value
-- * Exception handling
-- =========================================================

CREATE OR REPLACE FUNCTION calculate_order_total(p_orderid INT)
RETURNS NUMERIC
LANGUAGE plpgsql
AS $$
DECLARE
    total_price NUMERIC := 0;
    item_record RECORD;
BEGIN

    FOR item_record IN
        SELECT quantity, subtotal
        FROM orderitem
        WHERE orderid = p_orderid
    LOOP

        total_price := total_price + item_record.subtotal;

    END LOOP;

    RETURN total_price;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error while calculating total: %', SQLERRM;
        RETURN -1;
END;
$$;

--SELECT calculate_order_total(1);