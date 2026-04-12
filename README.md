# Rami Levy Online Store

**Maayan Schwartz & Ravid Davidovich**

---

## Table of Contents

1. Project Overview
2. System Description
3. Screens Design
4. Database Design (ERD & DSD)
5. Data Types and Constraints
6. Data Insertion Methods
7. Data Volume
8. Data Dictionary
9. SQL Scripts
10. Backup and Restore
11. Conclusion

---

## Project Overview

As part of the semester project, we designed and implemented a database system based on the **Rami Levy Hashikma Marketing online store**.

The goal of the project is to simulate a real-world supermarket system that manages customers, products, orders, suppliers, and inventory efficiently.

---

## System Description

The system supports the following main functionalities:

* Customer management
* Product and category management
* Order processing and tracking
* Supplier and inventory management
* Large-scale data handling

---

## Screens Design

## First Screen
![First Screen](DBProject/stage1/screenshots/firsterdplus.png)

## Second Screen
![Second Screen](DBProject/stage1/screenshots/dsd.png)

## Third Screen
![Third Screen](DBProject/stage1/screenshots/firstSiteAi.png)

[Click here to view the screen designs in Google AI Studio](https://ai.studio/apps/c41f5714-9418-42d2-864a-55b818c0d1db)

## Data Insertion Methods Screenshots

### Manual Insert (SQL)
This screenshot demonstrates inserting data manually using SQL `INSERT` statements.

![Manual Insert](DBProject/stage1/screenshots/insertPic.png)

---

### Python Generated Data
This screenshot shows the Python script used to generate large datasets automatically.

![Python Script](DBProject/stage1/screenshots/pyPic.png)

---

### CSV Import Method
This screenshot shows the CSV file used to import product data into the database.

![CSV File](DBProject/stage1/screenshots/csvPic.png)

---

## Backup and Restore

### Database Backup
This screenshot shows the execution of the database backup process using PostgreSQL.

![Backup](DBProject/stage1/screenshots/backup.png)

---

### Database Restore
This screenshot demonstrates restoring the database from the backup file.

![Restore](DBProject/stage1/screenshots/restorePic.png)
---

## Database Design (ERD & DSD)

The system was designed using a **Top-Down approach**:

1. Defining system requirements
2. Creating an ERD diagram
3. Converting ERD into DSD
4. Implementing the schema in PostgreSQL

The database includes entities such as:
Customer, Orders, OrderItem, Product, Store, Supplier, Category, Inventory.

Relationships were implemented using **Primary Keys and Foreign Keys**.

---

## Data Types and Constraints

* `VARCHAR` – text fields (names, emails, addresses)
* `INT` – identifiers and quantities
* `NUMERIC` – prices and totals
* `DATE` – dates

Constraints:

* Primary Keys
* Foreign Keys
* NOT NULL

---

## Data Insertion Methods

### 1. Manual Insert

Data was inserted manually for demonstration purposes.

File:

```
DBProject/stage1/manualInsert/manual_insert.sql
```

---

### 2. Python Generated Data

Large datasets were generated automatically using Python.

Tables populated:

* category (500)
* customer (500)
* orders (20000)
* orderitem (20000)
* store (500)
* supplier (500)
* inventory (500)
* belongs_to (500)
* supplies (500)
* located_in (500)
* orders_customer (20000)
* contains (20000)
* included_in (20000)

Location:

```
DBProject/stage1/Programing/
```

---

### 3. CSV Import

Products were generated using Python and saved as CSV.

Imported using:

```
COPY product(...)
```

File:

```
DBProject/stage1/DataImportFiles/products.csv
```

---

## Data Volume

* Minimum 500 records per table
* 20,000 records in large tables (orders, orderitem)

---

## Data Dictionary

### Customer

Stores customer details

* customerid – unique ID
* customername – customer name
* email – email address
* phone – phone number
* city – city
* street – street

---

### Orders

Stores order information

* orderid – unique order ID
* orderdate – date of order
* totalamount – total price
* orderstatus – order status
* paymentmethod – payment type

---

### OrderItem

Stores items in each order

* orderitemid – unique ID
* quantity – amount of product
* subtotal – price for item
* inonsale – sale indicator
* saledescription – sale description

---

### Product

Stores product data

* productid – unique ID
* productname – name
* price – product price
* dateofmanufacture – production date
* expirationdate – expiration date
* kashrut – certification

---

### Store

Stores branch information

* storeid – unique ID
* storename – branch name
* phone – phone number
* websiteurl – website
* rating – rating

---

### Supplier

Stores supplier information

* supplierid – unique ID
* suppliername – supplier name
* email – email
* phone – phone
* city – city
* street – street

---

### Category

Stores product categories

* categoryid – unique ID
* categoryname – category name

---

### Inventory

Stores stock information

* productid – product reference
* quantity – stock quantity
* minimumstock – minimum stock

---

### Relationships Tables

#### belongs_to

* productid
* categoryid

#### supplies

* supplierid
* productid

#### located_in

* storeid
* productid

#### orders_customer

* customerid
* orderid

#### contains

* orderid
* orderitemid

#### included_in

* productid
* orderitemid

---

## SQL Scripts

* createTables.sql
* dropTables.sql
* insertTables.sql
* selectAll.sql

---

## Backup and Restore

Backup file:

```
DBProject/stage1/backup.sql
```

The backup was successfully tested.

---

## Conclusion

This project demonstrates full database development including:

* Design (ERD & DSD)
* Implementation
* Data generation
* Multiple insertion methods
* Real-world simulation

The system is scalable and represents a realistic supermarket database.

---
