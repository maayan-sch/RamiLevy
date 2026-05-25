-- =====================================================
-- Integrate.sql
-- =====================================================


-- =====================================================
-- STORE INTEGRATION
-- =====================================================

-- Add new column from Tova's system
ALTER TABLE public.store

-- Update existing stores with Tova's data
UPDATE public.store s
SET
    rating = sb.rating
FROM public.storeb sb
WHERE s.storeid = sb.storeid;

-- Insert stores that do not exist yet
INSERT INTO public.store
(storeid, storename, phone, websiteurl, rating)

SELECT
    sb.storeid,
    sb.storename,
    sb.phone,
    NULL,
    sb.rating

FROM public.storeb sb

WHERE NOT EXISTS (
    SELECT 1
    FROM public.store s
    WHERE s.storeid = sb.storeid
);


-- =====================================================
-- PRODUCT INTEGRATION
-- =====================================================

ALTER TABLE public.product
ADD COLUMN IF NOT EXISTS brand VARCHAR(50);

-- Update existing products
UPDATE public.product p
SET
    brand = pb.brand
FROM public.productb pb
WHERE p.productid = pb.productid;

-- Insert new products
INSERT INTO public.product
(
    productid,
    productname,
    price,
    dateofmanufacture,
    expirationdate,
    kashrut,
    categoryid,
    supplierid,
    brand
)

SELECT
    pb.productid,
    pb.productname,
    pb.price,
    CURRENT_DATE,
    pb.expirationdate,
    pb.kashrut,
    pb.categoryid,
    1,
    pb.brand

FROM public.productb pb

WHERE NOT EXISTS (
    SELECT 1
    FROM public.product p
    WHERE p.productid = pb.productid
);


-- =====================================================
-- INVENTORY INTEGRATION
-- =====================================================

INSERT INTO public.inventory
(productid, storeid, quantity, minimumstock)

SELECT
    ib.productid,
    ib.storeid,
    ib.quantity,
    ib.minimumstock

FROM public.inventoryb ib

WHERE EXISTS (
    SELECT 1
    FROM public.product p
    WHERE p.productid = ib.productid
)

AND EXISTS (
    SELECT 1
    FROM public.store s
    WHERE s.storeid = ib.storeid
)

AND NOT EXISTS (
    SELECT 1
    FROM public.inventory i
    WHERE i.productid = ib.productid
);


-- =====================================================
-- SUPPLIER INTEGRATION
-- =====================================================

-- Update supplier data
UPDATE public.supplier s
SET
    email = sb.email,
    phone = sb.contactphone
FROM public.supplierb sb
WHERE s.supplierid = sb.supplierid;

-- Insert new suppliers
INSERT INTO public.supplier
(
    supplierid,
    suppliername,
    email,
    phone,
    city,
    street
)

SELECT
    sb.supplierid,
    sb.suppliername,
    sb.email,
    sb.contactphone,
    'Unknown',
    'Unknown'

FROM public.supplierb sb

WHERE NOT EXISTS (
    SELECT 1
    FROM public.supplier s
    WHERE s.supplierid = sb.supplierid
);


-- =====================================================
-- LOCATION TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS public.location (
    locationid integer PRIMARY KEY,
    city character varying(100) NOT NULL,
    street character varying(100) NOT NULL,
    streetnumber integer NOT NULL
);

INSERT INTO public.location
(locationid, city, street, streetnumber)

SELECT
    lb.locationid,
    lb.city,
    lb.street,
    lb.streetnumber

FROM public.locationb lb

WHERE NOT EXISTS (
    SELECT 1
    FROM public.location l
    WHERE l.locationid = lb.locationid
);


-- =====================================================
-- REMOVE UNUSED TABLE
-- =====================================================

DROP TABLE IF EXISTS public.suppliered_by CASCADE;


-- =====================================================
-- CATEGORY UPDATE
-- =====================================================

ALTER TABLE public.category
ADD COLUMN IF NOT EXISTS isactive INT DEFAULT 1;




