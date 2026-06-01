-- =========================================================
-- Procedure: restock_inventory
-- Description:
-- This procedure checks the inventory table for products
-- whose quantity is lower than the minimum stock value.
-- The procedure automatically updates the inventory quantity
-- by adding additional stock.
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
CREATE OR REPLACE PROCEDURE restock_inventory()
LANGUAGE plpgsql
AS $$
DECLARE
    inventory_record RECORD;
BEGIN

    FOR inventory_record IN
        SELECT
            storeid,
            productid,
            quantity,
            minimumstock
        FROM inventory
        WHERE quantity < minimumstock
    LOOP

        UPDATE inventory
        SET quantity = minimumstock + 50
        WHERE storeid = inventory_record.storeid
          AND productid = inventory_record.productid;

        RAISE NOTICE
        'Inventory updated for product % in store %',
        inventory_record.productid,
        inventory_record.storeid;

    END LOOP;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error in restock procedure: %', SQLERRM;
END;
$$;

--before
/*SELECT
    storeid,
    productid,
    quantity,
    minimumstock
FROM inventory
WHERE quantity < minimumstock;*/

--CALL restock_inventory();

--after
/*
SELECT
    storeid,
    productid,
    quantity,
    minimumstock
FROM inventory
WHERE quantity >= minimumstock;*/

--togther
/*SELECT
    storeid,
    productid,
    minimumstock,
    quantity AS quantity_after_restock,
    quantity - (minimumstock + 50) + minimumstock AS estimated_quantity_before
FROM inventory
WHERE quantity = minimumstock + 50;*/