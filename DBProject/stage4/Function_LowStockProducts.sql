-- =========================================================
-- Function: get_low_stock_products
-- Description:
-- This function returns a REF CURSOR containing products
-- with low inventory quantity.
-- A product is considered low in stock when its quantity
-- is smaller than the minimum stock value.
--
-- Programming elements used:
-- * Function
-- * REF CURSOR
-- * JOIN
-- * RETURN CURSOR
-- * Exception handling
-- =========================================================

CREATE OR REPLACE FUNCTION get_low_stock_products()
RETURNS REFCURSOR
LANGUAGE plpgsql
AS $$
DECLARE
    low_stock_cursor REFCURSOR := 'low_stock_cursor';
BEGIN

    OPEN low_stock_cursor FOR
        SELECT
            p.productid,
            p.productname,
            i.quantity,
            i.minimumstock
        FROM product p
        JOIN inventory i
            ON p.productid = i.productid
        WHERE i.quantity < i.minimumstock;

    RETURN low_stock_cursor;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error in low stock function: %', SQLERRM;
        RETURN NULL;
END;
$$;

/*BEGIN;

SELECT get_low_stock_products();

FETCH ALL IN "low_stock_cursor";*/