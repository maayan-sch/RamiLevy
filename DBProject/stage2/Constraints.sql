-- Constraint 1: Product price must be positive
ALTER TABLE product
ADD CONSTRAINT price_positive CHECK (price > 0);

-- Test Constraint 1
INSERT INTO product (productid, productname, price, dateofmanufacture, expirationdate, kashrut, categoryid, supplierid)
VALUES (9999, 'TestProduct', -10, '2024-01-01', '2025-01-01', 'Kosher', 1, 1);

-- Constraint 2: Quantity must be non-negative
ALTER TABLE inventory
ADD CONSTRAINT quantity_non_negative CHECK (quantity >= 0);

-- Test Constraint 2
INSERT INTO inventory (productid, storeid, quantity, minimumstock)
VALUES (1, 1, -5, 10);

-- Constraint 3: Store rating must be between 1 and 5
ALTER TABLE store
ADD CONSTRAINT rating_range CHECK (rating BETWEEN 1 AND 5);

-- Test Constraint 3
INSERT INTO store (storeid, storename, phone, websiteurl, rating)
VALUES (998, 'TestStore', '0500000000', 'test.com', 6);