-- =====================================
-- INSERT TABLES - Stage 1
-- Rami Levy DB Project
-- =====================================

-- =========================
-- Method 1: Manual Insert
-- =========================

-- Category table populated manually
-- File:
-- DBProject/stage1/manualInsert/manual_insert.sql


-- =========================
-- Method 2: Python Generated Data
-- =========================

-- The following tables were populated using Python scripts:
-- customer (500 records)
-- orders (20000 records)
-- orderitem (20000 records)
-- store (500 records)
-- supplier (500 records)
-- inventory (500 records)
-- belongs_to (500 records)
-- supplies (500 records)
-- located_in (500 records)
-- orders_customer (20000 records)
-- contains (20000 records)
-- included_in (20000 records)

-- Files located in:
-- DBProject/stage1/Programing/


-- =========================
-- Method 3: CSV Import
-- =========================

-- Product table populated using CSV file
-- File:
-- DBProject/stage1/DataImportFiles/products.csv

COPY product(productid, productname, price, dateofmanufacture, expirationdate, kashrut)
FROM '/tmp/products.csv'
DELIMITER ','
CSV HEADER;