-- =========================================================
-- Procedure: update_expired_product_discount
-- Description:
-- This procedure updates product prices for products that
-- are close to their expiration date.
-- Products expiring within the next 30 days receive a 20%
-- discount on their current price.
--
-- Programming elements used:
-- * Procedure
-- * FOR LOOP
-- * RECORD
-- * UPDATE statement
-- * Variables
-- * RAISE NOTICE
-- * Exception handling
-- =========================================================

CREATE OR REPLACE PROCEDURE update_expired_product_discount()
LANGUAGE plpgsql
AS $$
DECLARE
    product_record RECORD;
BEGIN

    FOR product_record IN
        SELECT
            productid,
            productname,
            expirationdate,
            price
        FROM product
        WHERE expirationdate <= CURRENT_DATE + INTERVAL '30 days'
    LOOP

        UPDATE product
        SET price = price * 0.80
        WHERE productid = product_record.productid;

        RAISE NOTICE 'Discount updated for product: %',
            product_record.productname;

    END LOOP;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error updating discounts: %', SQLERRM;
END;
$$;

--CALL update_expired_product_discount();

/*SELECT
    productid,
    productname,
    price AS price_after_discount,
    ROUND(price / 0.80, 2) AS estimated_price_before_discount,
    expirationdate
FROM product
WHERE expirationdate <= CURRENT_DATE + INTERVAL '30 days';*/