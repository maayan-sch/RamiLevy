import random
import csv
from datetime import datetime, timedelta

# =========================
# Customers - 500
# =========================
with open(r"DBProject\stage1\Programing\customers_inserts.sql", "w", encoding="utf-8") as f:
    for i in range(1, 501):
        f.write(
            f"INSERT INTO customer (customerid, customername, email, phone, city, street) VALUES "
            f"({i}, 'Customer{i}', 'customer{i}@mail.com', '050{i:07d}', 'City{i%10}', 'Street {i}');\n"
        )

# =========================
# Orders - 20,000
# =========================
with open(r"DBProject\stage1\Programing\orders_inserts.sql", "w", encoding="utf-8") as f:
    statuses = ["Pending", "Completed", "Cancelled", "Shipped"]
    methods = ["Credit Card", "Cash", "Bit", "PayPal"]

    for i in range(1, 20001):
        customer = ((i - 1) % 500) + 1
        status = statuses[(i - 1) % len(statuses)]
        method = methods[(i - 1) % len(methods)]

        f.write(
            f"INSERT INTO orders (orderid, orderdate, totalamount, orderstatus, paymentmethod, customerid) VALUES "
            f"({i}, '2025-01-{((i - 1) % 28) + 1:02d}', {random.randint(20,500)}, '{status}', '{method}', {customer});\n"
        )

# =========================
# OrderItem - 20,000
# =========================
with open(r"DBProject\stage1\Programing\orderitem_inserts.sql", "w", encoding="utf-8") as f:
    for i in range(1, 20001):
        order_id = i
        product_id = ((i - 1) % 500) + 1

        f.write(
            f"INSERT INTO orderitem (orderitemid, orderid, quantity, subtotal, inonsale, saledescription, productid) VALUES "
            f"({i}, {order_id}, {random.randint(1,5)}, {random.randint(10,200)}, FALSE, NULL, {product_id});\n"
        )

# =========================
# Store - 500
# =========================
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

# =========================
# Supplier - 500
# =========================
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

# =========================
# Inventory - 500
# =========================
with open(r"DBProject\stage1\Programing\inventory_inserts.sql", "w", encoding="utf-8") as f:
    for i in range(1, 501):
        store_id = ((i - 1) % 500) + 1
        f.write(
            f"INSERT INTO inventory (productid, storeid, quantity, minimumstock) VALUES "
            f"({i}, {store_id}, {i * 2}, 10);\n"
        )

# =========================
# Products CSV - 500
# =========================
def random_date():
    start = datetime(2024, 1, 1)
    end = datetime(2025, 12, 31)
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).strftime("%Y-%m-%d")

with open(r"DBProject\stage1\DataImportFiles\products.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "productid", "productname", "price",
        "dateofmanufacture", "expirationdate",
        "kashrut", "categoryid", "supplierid"
    ])

    for i in range(1, 501):
        category = ((i - 1) % 5) + 1
        supplier = ((i - 1) % 500) + 1

        writer.writerow([
            i,
            f"Product{i}",
            round(random.uniform(5, 100), 2),
            random_date(),
            random_date(),
            "Rabbanut",
            category,
            supplier
        ])