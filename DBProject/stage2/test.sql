-- Query 2A: Products with quantity below minimum stock (using JOIN)
SELECT
    p.productid,
    p.productname,
    s.suppliername,
    EXTRACT(YEAR FROM p.expirationdate) AS exp_year,
    EXTRACT(MONTH FROM p.expirationdate) AS exp_month,
    p.price
FROM product p
JOIN supplier s ON p.supplierid = s.supplierid
WHERE p.price > 50
ORDER BY exp_year, exp_month;



-- Query 2B: Products with quantity below minimum stock (using EXISTS)
SELECT
    p.productid,
    p.productname,
    s.suppliername,
    EXTRACT(YEAR FROM p.expirationdate) AS exp_year,
    EXTRACT(MONTH FROM p.expirationdate) AS exp_month,
    p.price
FROM product p
JOIN supplier s ON p.supplierid = s.supplierid
WHERE EXISTS (
    SELECT 1
    FROM product p2
    WHERE p2.productid = p.productid
      AND p2.price > 50
)
ORDER BY exp_year, exp_month;
