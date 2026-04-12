import random

# ----- Customers -----
with open("customers_inserts.sql", "w", encoding="utf-8") as f:
    for i in range(1, 501):
        f.write(
            f"INSERT INTO customer (customerid, customername, email, phone, city, street) VALUES "
            f"({i}, 'Customer{i}', 'customer{i}@mail.com', '050{i:07d}', 'City{i%10}', 'Street {i}');\n"
        )

# ----- Orders -----
with open("orders_inserts.sql", "w", encoding="utf-8") as f:
    for i in range(1, 20001):
        f.write(
            f"INSERT INTO orders (orderid, orderdate, totalamount, orderstatus, paymentmethod) VALUES "
            f"({i}, '2025-01-01', {random.randint(20,500)}, 'Completed', 'Credit');\n"
        )

# ----- OrderItem -----
with open("orderitem_inserts.sql", "w", encoding="utf-8") as f:
    for i in range(1, 20001):
        f.write(
            f"INSERT INTO orderitem (orderitemid, quantity, subtotal, inonsale, saledescription) VALUES "
            f"({i}, {random.randint(1,5)}, {random.randint(10,200)}, false, NULL);\n"
        )
        

# ----- Stores -----
with open(r"DBProject\stage1\Programing\store_inserts.sql", "w", encoding="utf-8") as f:
    cities = [
        "Jerusalem", "Tel Aviv", "Haifa", "Rishon LeZion", "Petah Tikva",
        "Ashdod", "Netanya", "Beersheba", "Holon", "Rehovot"
    ]

    for i in range(1, 501):
        city = cities[(i - 1) % len(cities)]
        f.write(
            f"INSERT INTO store (storeid, storename, phone, websiteurl, rating) VALUES "
            f"({i}, 'Rami Levy {city} Branch {i}', '05{i:08d}', 'www.rami-levy.co.il', {(i % 5) + 1});\n"
        )

# ----- Suppliers -----
with open(r"DBProject\stage1\Programing\supplier_inserts.sql", "w", encoding="utf-8") as f:
    supplier_names = [
        "Tnuva", "Osem", "Strauss", "Unilever Israel", "Diplomat",
        "Sano", "Tara", "Sugat", "Yotvata", "Nestle Israel"
    ]
    cities = [
        "Petah Tikva", "Shoham", "Holon", "Haifa", "Jerusalem",
        "Ashdod", "Netanya", "Rehovot", "Beersheba", "Rishon LeZion"
    ]

    for i in range(1, 501):
        name = supplier_names[(i - 1) % len(supplier_names)]
        city = cities[(i - 1) % len(cities)]
        f.write(
            f"INSERT INTO supplier (supplierid, suppliername, email, phone, city, street) VALUES "
            f"({i}, '{name} Supplier {i}', 'supplier{i}@mail.com', '03{i:07d}', '{city}', 'Industrial Street {i}');\n"
        )
        
# ----- inventory -----
with open(r"DBProject\stage1\Programing\inventory_inserts.sql", "w") as f:
    for i in range(1, 501):
        f.write(f"INSERT INTO inventory (productid, quantity, minimumstock) VALUES ({i}, {i*2}, 10);\n")

# ----- belongs_to -----
with open(r"DBProject\stage1\Programing\belongs_to_inserts.sql", "w") as f:
    for i in range(1, 501):
        category = (i % 5) + 1
        f.write(f"INSERT INTO belongs_to (productid, categoryid) VALUES ({i}, {category});\n")

# ----- supplies -----
with open(r"DBProject\stage1\Programing\supplies_inserts.sql", "w") as f:
    for i in range(1, 501):
        supplier = (i % 500) + 1
        f.write(f"INSERT INTO supplies (supplierid, productid) VALUES ({supplier}, {i});\n")

# ----- located_in -----
with open(r"DBProject\stage1\Programing\located_in_inserts.sql", "w") as f:
    for i in range(1, 501):
        store = (i % 500) + 1
        f.write(f"INSERT INTO located_in (storeid, productid) VALUES ({store}, {i});\n")

# ----- orders_customer -----
with open(r"DBProject\stage1\Programing\orders_customer_inserts.sql", "w") as f:
    for i in range(1, 20001):
        customer = (i % 500) + 1
        f.write(f"INSERT INTO orders_customer (customerid, orderid) VALUES ({customer}, {i});\n")

# ----- contains -----
with open(r"DBProject\stage1\Programing\contains_inserts.sql", "w") as f:
    for i in range(1, 20001):
        f.write(f"INSERT INTO contains (orderid, orderitemid) VALUES ({i}, {i});\n")

# ----- included_in -----
with open(r"DBProject\stage1\Programing\included_in_inserts.sql", "w") as f:
    for i in range(1, 20001):
        product = (i % 500) + 1
        f.write(f"INSERT INTO included_in (productid, orderitemid) VALUES ({product}, {i});\n")
  # ----- csv-----      
import csv
import random
from datetime import datetime, timedelta

def random_date():
    start = datetime(2024, 1, 1)
    end = datetime(2025, 12, 31)
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).strftime("%Y-%m-%d")

with open(r"DBProject\stage1\DataImportFiles\products.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["productid", "productname", "price", "dateofmanufacture", "expirationdate", "kashrut"])

    for i in range(1, 501):
        writer.writerow([
            i,
            f"Product{i}",
            round(random.uniform(5, 100), 2),
            random_date(),
            random_date(),
            "Rabbanut"
        ])
        