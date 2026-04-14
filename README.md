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

As part of the semester project, we designed and implemented a database system based on the Rami Levy Hashikma Marketing online store.

The goal of the project is to simulate a real-world supermarket system that manages customers, products, categories, suppliers, stores, orders, and inventory efficiently.

---

## System Description

The system supports the following main functionalities:

- Customer management  
- Product and category management  
- Supplier and store management  
- Order processing and tracking  
- Inventory management  
- Handling large-scale data  

---

## Screens Design

## First Screen
![First Screen](DBProject/stage1/screenshots/firsterdplus.png)

## Second Screen
![Second Screen](DBProject/stage1/screenshots/dsd.png)

## Third Screen
![Third Screen](DBProject/stage1/screenshots/firstSiteAi.png)

[Click here to view the screen designs in Google AI Studio](https://ai.studio/apps/c41f5714-9418-42d2-864a-55b818c0d1db)

---

## Data Insertion Methods Screenshots

### Manual Insert (SQL)
![Manual Insert](DBProject/stage1/screenshots/insertPic.png)

### Python Generated Data
![Python Script](DBProject/stage1/screenshots/pyPic.png)

### CSV Import Method
![CSV File](DBProject/stage1/screenshots/csvPic.png)

---

## Backup and Restore

### Database Backup
![Backup](DBProject/stage1/screenshots/backup.png)

### Database Restore
![Restore](DBProject/stage1/screenshots/restorePic.png)

The backup was created using pg_dump and restored using psql inside Docker.

---

## Database Design (ERD & DSD)

The system was designed using a Top-Down approach:

- System requirements definition  
- ERD creation  
- Conversion to DSD  
- Implementation in PostgreSQL  

The schema was checked and is normalized to at least Third Normal Form (3NF).

The final database includes the following entities:

- Customer  
- Category  
- Store  
- Supplier  
- Product  
- Orders  
- OrderItem  
- Inventory  

Relationships are implemented using Foreign Keys inside the tables.

---

## Data Types and Constraints

- VARCHAR – text fields  
- INT – identifiers and quantities  
- NUMERIC – prices and totals  
- DATE – date fields  

Constraints:

- Primary Keys  
- Foreign Keys  
- NOT NULL  

---

## Data Insertion Methods

### 1. Manual Insert
Used for inserting category data.

File:
DBProject/stage1/manualInsert/manual_insert.sql

---

### 2. Python Generated Data
Used to generate large datasets automatically.

Tables populated:

- customer (500)  
- store (500)  
- supplier (500)  
- inventory (500)  
- orders (20000)  
- orderitem (20000)  

Location:
DBProject/stage1/Programing/

---

### 3. CSV Import
Used for inserting product data using the COPY command.

File:
DBProject/stage1/DataImportFiles/products.csv

---

## Data Volume

- Minimum 500 records per table  
- 20,000 records in orders and orderitem  

---

## Data Dictionary

### Customer
- customerid – unique ID  
- customername – name  
- email – email  
- phone – phone  
- city – city  
- street – street  

### Category
- categoryid – unique ID  
- categoryname – category name  

### Store
- storeid – unique ID  
- storename – branch name  
- phone – phone  
- websiteurl – website  
- rating – rating  

### Supplier
- supplierid – unique ID  
- suppliername – name  
- email – email  
- phone – phone  
- city – city  
- street – street  

### Product
- productid – unique ID  
- productname – name  
- price – price  
- dateofmanufacture – production date  
- expirationdate – expiration date  
- kashrut – certification  
- categoryid – FK  
- supplierid – FK  

### Orders
- orderid – unique ID  
- orderdate – date  
- totalamount – total price  
- orderstatus – status  
- paymentmethod – payment type  
- customerid – FK  

### OrderItem
- orderitemid – unique ID  
- orderid – FK  
- productid – FK  
- quantity – quantity  
- subtotal – price  
- inonsale – boolean  
- saledescription – description  

### Inventory
- productid – FK  
- storeid – FK  
- quantity – stock  
- minimumstock – minimum stock  

---

## SQL Scripts

- createTables.sql  
- dropTables.sql  
- insertTables.sql  
- selectAll.sql  

---

## Conclusion

This project demonstrates:

- Database design using ERD and DSD  
- Implementation in PostgreSQL  
- Data generation using multiple methods  
- Backup and restore processes  

The system is structured and simulates a real-world supermarket database.