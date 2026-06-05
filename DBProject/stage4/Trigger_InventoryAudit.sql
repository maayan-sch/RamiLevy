-- ============================================================
-- Trigger: Inventory Audit
-- Description:
-- Logs inventory quantity changes after UPDATE.
-- ============================================================

CREATE TABLE IF NOT EXISTS inventory_audit_log (
    logid SERIAL PRIMARY KEY,
    productid INT,
    oldquantity INT,
    newquantity INT,
    changedate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION log_inventory_changes()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN

    INSERT INTO inventory_audit_log
    (
        productid,
        oldquantity,
        newquantity
    )
    VALUES
    (
        OLD.productid,
        OLD.quantity,
        NEW.quantity
    );

    RETURN NEW;

END;
$$;

CREATE TRIGGER trg_inventory_audit
AFTER UPDATE OF quantity
ON inventory
FOR EACH ROW
EXECUTE FUNCTION log_inventory_changes();