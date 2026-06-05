-- ============================================================
-- Trigger: Order Status Log
-- Description:
-- Logs every order status change.
-- ============================================================

CREATE TABLE IF NOT EXISTS order_status_log (
    logid SERIAL PRIMARY KEY,
    orderid INT,
    oldstatus VARCHAR(50),
    newstatus VARCHAR(50),
    changedate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION log_order_status_change()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN

    INSERT INTO order_status_log
    (
        orderid,
        oldstatus,
        newstatus
    )
    VALUES
    (
        OLD.orderid,
        OLD.orderstatus,
        NEW.orderstatus
    );

    RETURN NEW;

END;
$$;

CREATE TRIGGER trg_order_status_log
AFTER UPDATE OF orderstatus
ON orders
FOR EACH ROW
EXECUTE FUNCTION log_order_status_change();