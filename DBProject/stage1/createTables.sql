CREATE TABLE customer (
  customerid INT PRIMARY KEY,
  customername VARCHAR(100) NOT NULL,
  email VARCHAR(100),
  phone VARCHAR(20) NOT NULL,
  city VARCHAR(50) NOT NULL,
  street VARCHAR(100) NOT NULL
);

CREATE TABLE category (
  categoryid INT PRIMARY KEY,
  categoryname VARCHAR(100) NOT NULL
);

CREATE TABLE store (
  storeid INT PRIMARY KEY,
  storename VARCHAR(100) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  websiteurl VARCHAR(255),
  rating NUMERIC(2,1)
);

CREATE TABLE supplier (
  supplierid INT PRIMARY KEY,
  suppliername VARCHAR(100) NOT NULL,
  email VARCHAR(100),
  phone VARCHAR(20) NOT NULL,
  city VARCHAR(50) NOT NULL,
  street VARCHAR(100) NOT NULL
);

CREATE TABLE product (
  productid INT PRIMARY KEY,
  productname VARCHAR(100) NOT NULL,
  price NUMERIC(10,2) NOT NULL,
  dateofmanufacture DATE NOT NULL,
  expirationdate DATE NOT NULL,
  kashrut VARCHAR(50) NOT NULL,
  categoryid INT NOT NULL,
  supplierid INT NOT NULL,
  FOREIGN KEY (categoryid) REFERENCES category(categoryid),
  FOREIGN KEY (supplierid) REFERENCES supplier(supplierid)
);

CREATE TABLE orders (
  orderid INT PRIMARY KEY,
  orderdate DATE NOT NULL,
  totalamount NUMERIC(10,2) NOT NULL,
  orderstatus VARCHAR(50) NOT NULL,
  paymentmethod VARCHAR(50) NOT NULL,
  customerid INT NOT NULL,
  FOREIGN KEY (customerid) REFERENCES customer(customerid)
);

CREATE TABLE orderitem (
  orderitemid INT NOT NULL,
  orderid INT NOT NULL,
  productid INT NOT NULL,
  quantity INT NOT NULL,
  subtotal NUMERIC(10,2) NOT NULL,
  inonsale BOOLEAN NOT NULL,
  saledescription VARCHAR(255),
  PRIMARY KEY (orderid,orderitemid),
  FOREIGN KEY (orderid) REFERENCES orders(orderid),
  FOREIGN KEY (productid) REFERENCES product(productid)
);

CREATE TABLE inventory (
  productid INT PRIMARY KEY,
  storeid INT NOT NULL,
  quantity INT NOT NULL,
  minimumstock INT NOT NULL,
  FOREIGN KEY (productid) REFERENCES product(productid),
  FOREIGN KEY (storeid) REFERENCES store(storeid)
);