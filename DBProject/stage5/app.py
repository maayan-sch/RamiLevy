import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from db_config import get_connection
from PIL import Image, ImageTk
from psycopg2 import sql


# ==================================================
# Database Connection Test
# ==================================================

def test_connection():
    try:
        conn = get_connection()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Connected to database successfully!"
        )

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


# ==================================================
# Products Screen
# ==================================================

def open_products():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.productid,
                p.productname,
                p.price,
                c.categoryname,
                s.suppliername,
                p.brand,
                p.dateofmanufacture,
                p.expirationdate,
                p.kashrut
            FROM product p
            JOIN category c
                ON p.categoryid = c.categoryid
            JOIN supplier s
                ON p.supplierid = s.supplierid
            ORDER BY p.productid
        """)

        rows = cursor.fetchall()

        products_window = tk.Toplevel(root)
        products_window.title("Products")
        products_window.geometry("1000x600")

        title = tk.Label(
            products_window,
            text="Products",
            font=("Arial", 16, "bold")
        )

        title.pack(pady=10)

        # CRUD Buttons
        buttons_frame = tk.Frame(products_window)
        buttons_frame.pack(pady=10)

        tk.Button(
            buttons_frame,
            text="Add Product",
            width=15,
            command=open_add_product
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            buttons_frame,
            text="Update Product",
            width=15,
            command=open_update_product
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            buttons_frame,
            text="Delete Product",
            width=15,
            command=open_delete_product
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            buttons_frame,
            text="Refresh",
            width=15,
            command=lambda: load_products(tree)
        ).pack(side=tk.LEFT, padx=5)

        tree = ttk.Treeview(
            products_window,
            columns=(
                "Product Name",
                "Price",
                "Category",
                "Supplier",
                "Brand",
                "Dateofmanufacture",
                "Expirationdate",
                "Kashrut"

            ),
            show="headings"
        )

        tree.heading(
            "Product Name",
            text="Product Name"
        )

        tree.heading(
            "Price",
            text="Price"
        )

        tree.heading(
            "Category",
            text="Category"
        )

        tree.heading(
            "Supplier",
            text="Supplier"
        )

        tree.heading(
            "Brand",
            text="Brand"
        )
        tree.heading(
        "Dateofmanufacture",
        text="Manufacture Date"
        )

        tree.heading(
            "Expirationdate",
            text="Expiration Date"
        )

        tree.heading(
            "Kashrut",
            text="Kashrut"
        )

        tree.column(
            "Product Name",
            width=250
        )

        tree.column(
            "Price",
            width=100
        )

        tree.column(
            "Category",
            width=200
        )

        tree.column(
            "Supplier",
            width=220
        )

        tree.column(
            "Brand",
            width=150
        )

        for row in rows:

            tree.insert(
                "",
                tk.END,
                values=(
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6],
                    row[7],
                    row[8]
                )
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )
        load_products(tree)

        conn.close()

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )



def load_products(tree):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.productid,
            p.productname,
            p.price,
            c.categoryname,
            s.suppliername,
            p.brand,
            p.dateofmanufacture,
            p.expirationdate,
            p.kashrut
        FROM product p
        JOIN category c
            ON p.categoryid = c.categoryid
        JOIN supplier s
            ON p.supplierid = s.supplierid
        ORDER BY p.productid DESC
    """)

    rows = cursor.fetchall()

    for item in tree.get_children():
        tree.delete(item)

    for row in rows:
        tree.insert(
            "",
            tk.END,
            values=(
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8]
            )
        )

    conn.close()


def open_products_view():

    try:
        products_window = tk.Toplevel(root)
        products_window.title("Products - View Only")
        products_window.geometry("1000x600")

        title = tk.Label(
            products_window,
            text="Products - View Only",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        tree = ttk.Treeview(
            products_window,
            columns=(
                "Product Name",
                "Price",
                "Category",
                "Supplier",
                "Brand",
                "Dateofmanufacture",
                "Expirationdate",
                "Kashrut"
            ),
            show="headings"
        )

        tree.heading("Product Name", text="Product Name")
        tree.heading("Price", text="Price")
        tree.heading("Category", text="Category")
        tree.heading("Supplier", text="Supplier")
        tree.heading("Brand", text="Brand")
        tree.heading("Dateofmanufacture", text="Manufacture Date")
        tree.heading("Expirationdate", text="Expiration Date")
        tree.heading("Kashrut", text="Kashrut")

        tree.column("Product Name", width=250)
        tree.column("Price", width=100)
        tree.column("Category", width=200)
        tree.column("Supplier", width=220)
        tree.column("Brand", width=150)
        tree.column("Dateofmanufacture", width=150)
        tree.column("Expirationdate", width=150)
        tree.column("Kashrut", width=120)

        tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        load_products(tree)

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )

def open_add_product():

    add_window = tk.Toplevel(root)

    add_window.title("Add Product")
    add_window.geometry("500x500")

    tk.Label(add_window, text="Product Name").pack()
    name_entry = tk.Entry(add_window)
    name_entry.pack()

    tk.Label(add_window, text="Price").pack()
    price_entry = tk.Entry(add_window)
    price_entry.pack()

    tk.Label(add_window, text="Brand").pack()
    brand_entry = tk.Entry(add_window)
    brand_entry.pack()

    tk.Label(add_window, text="Kashrut").pack()
    kashrut_entry = tk.Entry(add_window)
    kashrut_entry.pack()

    tk.Label(add_window, text="Manufacture Date (YYYY-MM-DD)").pack()
    manufacture_entry = tk.Entry(add_window)
    manufacture_entry.pack()

    tk.Label(add_window, text="Expiration Date (YYYY-MM-DD)").pack()
    expiration_entry = tk.Entry(add_window)
    expiration_entry.pack()

    def save_product():

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT COALESCE(MAX(productid),0)+1
                FROM product
            """)

            new_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO product
                (
                    productid,
                    productname,
                    price,
                    categoryid,
                    supplierid,
                    brand,
                    kashrut,
                    dateofmanufacture,
                    expirationdate
                )
                VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                new_id,
                name_entry.get(),
                float(price_entry.get()),
                1,
                1,
                brand_entry.get(),
                kashrut_entry.get(),
                manufacture_entry.get(),
                expiration_entry.get()
            ))

            conn.commit()

            conn.close()

            messagebox.showinfo(
                "Success",
                "Product added successfully"
            )
            add_window.destroy()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    tk.Button(
        add_window,
        text="Save Product",
        command=save_product
    ).pack(pady=20)
    

def open_update_product():

    update_window = tk.Toplevel(root)
    update_window.title("Update Product")
    update_window.geometry("500x500")

    tk.Label(update_window, text="Product Name").pack()

    name_entry = tk.Entry(update_window)
    name_entry.pack()

    tk.Label(update_window, text="Brand").pack()

    brand_entry = tk.Entry(update_window)
    brand_entry.pack()

    tk.Label(update_window, text="Price").pack()

    price_entry = tk.Entry(update_window)
    price_entry.pack()

    def load_product():

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    productname,
                    price
                FROM product
                WHERE productname = %s
                  AND brand = %s
            """,
            (
                name_entry.get(),
                brand_entry.get()
            ))

            row = cursor.fetchone()
            conn.close()

            if row:
                price_entry.delete(0, tk.END)
                price_entry.insert(0, row[1])
            else:
                messagebox.showerror("Error", "Product not found")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_product():

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE product
                SET price = %s
                WHERE productname = %s
                  AND brand = %s
            """,
            (
                float(price_entry.get()),
                name_entry.get(),
                brand_entry.get()
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Product updated successfully")
            update_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(
        update_window,
        text="Load Product",
        command=load_product
    ).pack(pady=10)

    tk.Button(
        update_window,
        text="Update Product",
        command=update_product
    ).pack(pady=10)
    

def open_delete_product():

    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Product")
    delete_window.geometry("400x250")

    tk.Label(delete_window, text="Product Name").pack(pady=10)

    name_entry = tk.Entry(delete_window)
    name_entry.pack()

    tk.Label(delete_window, text="Brand").pack(pady=10)

    brand_entry = tk.Entry(delete_window)
    brand_entry.pack()

    def delete_product():

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM product
                WHERE productname = %s
                  AND brand = %s
            """,
            (
                name_entry.get(),
                brand_entry.get()
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Product deleted successfully")
            delete_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(
        delete_window,
        text="Delete Product",
        command=delete_product
    ).pack(pady=20)

# ==================================================
# Queries & Programs Screen
# ==================================================

def show_results(title, columns, rows):

    result_window = tk.Toplevel(root)

    result_window.title(title)

    result_window.geometry("1000x600")

    tk.Label(
        result_window,
        text=title,
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    frame = tk.Frame(result_window)

    frame.pack(
        fill="both",
        expand=True
    )

    tree = ttk.Treeview(
        frame,
        columns=columns,
        show="headings"
    )

    scrollbar_y = ttk.Scrollbar(
        frame,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scrollbar_y.set
    )

    for col in columns:

        tree.heading(
            col,
            text=col
        )

        tree.column(
            col,
            width=170,
            anchor="center"
        )

    for row in rows:

        tree.insert(
            "",
            tk.END,
            values=row
        )

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar_y.pack(
        side="right",
        fill="y"
    )

def run_total_sales_by_category():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                c.categoryname,
                COUNT(oi.orderitemid) AS total_items_sold,
                SUM(oi.subtotal) AS total_sales
            FROM category c
            JOIN product p ON c.categoryid = p.categoryid
            JOIN orderitem oi ON p.productid = oi.productid
            GROUP BY c.categoryid, c.categoryname
            ORDER BY total_sales DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        show_results(
            "Total Sales By Category",
            ("Category", "Total Items Sold", "Total Sales"),
            rows
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def run_expiring_products_query():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.productname,
                p.dateofmanufacture,
                p.expirationdate,
                p.price
            FROM product p
            WHERE p.expirationdate BETWEEN CURRENT_DATE
                                       AND CURRENT_DATE + INTERVAL '30 days'
            ORDER BY p.expirationdate
        """)

        rows = cursor.fetchall()
        conn.close()

        show_results(
            "Expired Or Soon-To-Expire Products",
            ("Product Name", "Manufacture Date", "Expiration Date", "Price"),
            rows
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def run_calculate_order_total():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT calculate_order_total(1)
        """)

        result = cursor.fetchone()[0]
        conn.close()

        messagebox.showinfo(
            "Order Total",
            f"Total amount for order 1 is: {result}"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def run_restock_inventory():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CALL restock_inventory()
        """)

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Restock inventory procedure executed successfully"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def run_update_expired_discounts():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CALL update_expired_product_discount()
        """)

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Expired product discount procedure executed successfully"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def open_suppliers():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                suppliername,
                phone,
                email
            FROM supplier
            ORDER BY suppliername
        """)

        rows = cursor.fetchall()

        window = tk.Toplevel(root)

        window.title("Suppliers")
        window.geometry("800x500")

        tree = ttk.Treeview(
            window,
            columns=(
                "Supplier Name",
                "Phone",
                "Email"
            ),
            show="headings"
        )

        tree.heading(
            "Supplier Name",
            text="Supplier Name"
        )

        tree.heading(
            "Phone",
            text="Phone"
        )

        tree.heading(
            "Email",
            text="Email"
        )

        for row in rows:

            tree.insert(
                "",
                tk.END,
                values=row
            )

        tree.pack(
            fill="both",
            expand=True
        )

        conn.close()

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

def open_inventory():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.productname,
                s.storename,
                i.quantity,
                i.minimumstock
            FROM inventory i
            JOIN product p
                ON i.productid = p.productid
            JOIN store s
                ON i.storeid = s.storeid
            ORDER BY p.productname
        """)

        rows = cursor.fetchall()

        window = tk.Toplevel(root)

        window.title("Inventory")
        window.geometry("900x500")

        tree = ttk.Treeview(
            window,
            columns=(
                "Product",
                "Store",
                "Quantity",
                "Minimum Stock"
            ),
            show="headings"
        )

        tree.heading(
            "Product",
            text="Product"
        )

        tree.heading(
            "Store",
            text="Store"
        )

        tree.heading(
            "Quantity",
            text="Quantity"
        )

        tree.heading(
            "Minimum Stock",
            text="Minimum Stock"
        )

        for row in rows:

            tree.insert(
                "",
                tk.END,
                values=row
            )

        tree.pack(
            fill="both",
            expand=True
        )

        conn.close()

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

def open_customers():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                customername,
                email,
                phone,   
                city,
                street
            FROM customer
            ORDER BY customername
        """)

        rows = cursor.fetchall()
        conn.close()

        show_results(
            "Customers",
            ("Customer Name", "Email", "Phone","City","Street"),
            rows
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))
        
def open_orders():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                c.customername,
                o.orderdate,
                o.totalamount,
                o.orderstatus,
                o.paymentmethod
            FROM orders o
            JOIN customer c
                ON o.customerid = c.customerid
            ORDER BY o.orderdate DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        show_results(
            "Orders",
            ("Customer", "Order Date", "Total Amount", "Status","Paymentmethod"),
            rows
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))
        
def open_stores():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                storename,
                phone,
                websiteurl,
                rating
            FROM store
            ORDER BY storename
        """)

        rows = cursor.fetchall()
        conn.close()

        show_results(
            "Stores",
            (
                "Store Name",
                "Phone",
                "Website",
                "Rating"
            ),
            rows
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )        


def open_categories():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                categoryname,
                isactive
            FROM category
            ORDER BY categoryname
        """)

        rows = cursor.fetchall()
        conn.close()

        show_results(
            "Categories",
            ("Category Name", "Is Active"),
            rows
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def open_discounts():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                discountname,
                discountpercentage,
                startdate,
                enddate
            FROM discount
            ORDER BY discountname
        """)

        rows = cursor.fetchall()
        conn.close()

        show_results(
            "Discounts",
            ("Discount Name", "Discount %", "Start Date", "End Date"),
            rows
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def open_employees():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                e.firstname,
                e.lastname,
                e.status,
                e.salary,
                e.role,
                s.storename
            FROM employee e
            JOIN store s
                ON e.storeid = s.storeid
            ORDER BY e.firstname, e.lastname
        """)

        rows = cursor.fetchall()
        conn.close()

        show_results(
            "Employees",
            ("First Name", "Last Name", "Status", "Salary", "Role", "Store"),
            rows
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def open_locations():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                city,
                street,
                streetnumber
            FROM location
            ORDER BY city, street
        """)

        rows = cursor.fetchall()
        conn.close()

        show_results(
            "Locations",
            ("City", "Street", "Street Number"),
            rows
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def open_regions():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                regionname
            FROM region
            ORDER BY regionname
        """)

        rows = cursor.fetchall()
        conn.close()

        show_results(
            "Regions",
            ("Region Name",),
            rows
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def open_order_items():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                c.customername,
                o.orderdate,
                p.productname,
                oi.quantity,
                oi.subtotal,
                oi.inonsale,
                oi.saledescription
            FROM orderitem oi
            JOIN orders o
                ON oi.orderid = o.orderid
            JOIN customer c
                ON o.customerid = c.customerid
            JOIN product p
                ON oi.productid = p.productid
            ORDER BY o.orderdate DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        show_results(
            "Order Items",
            (
                "Customer",
                "Order Date",
                "Product",
                "Quantity",
                "Subtotal",
                "On Sale",
                "Sale Description"
            ),
            rows
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))

def open_applies_to():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.productname,
                d.discountname
            FROM applies_to a
            JOIN product p
                ON a.productid = p.productid
            JOIN discount d
                ON a.discountid = d.discountid
            ORDER BY p.productname
        """)

        rows = cursor.fetchall()
        conn.close()

        show_results(
            "Product Discounts",
            ("Product", "Discount"),
            rows
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def open_inventory_audit_log():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.productname,
                l.oldquantity,
                l.newquantity,
                l.changedate
            FROM inventory_audit_log l
            LEFT JOIN product p
                ON l.productid = p.productid
            ORDER BY l.changedate DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        show_results(
            "Inventory Audit Log",
            (
                "Product",
                "Old Quantity",
                "New Quantity",
                "Change Date"
            ),
            rows
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))

def open_order_status_log():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                c.customername,
                o.orderdate,
                l.oldstatus,
                l.newstatus,
                l.changedate
            FROM order_status_log l
            LEFT JOIN orders o
                ON l.orderid = o.orderid
            LEFT JOIN customer c
                ON o.customerid = c.customerid
            ORDER BY l.changedate DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        show_results(
            "Order Status Log",
            (
                "Customer",
                "Order Date",
                "Old Status",
                "New Status",
                "Change Date"
            ),
            rows
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))



def get_table_columns(table_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = %s
        ORDER BY ordinal_position
    """, (table_name,))

    columns = [row[0] for row in cursor.fetchall()]
    conn.close()
    return columns


def get_primary_keys(table_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
           AND tc.table_schema = kcu.table_schema
        WHERE tc.constraint_type = 'PRIMARY KEY'
          AND tc.table_schema = 'public'
          AND tc.table_name = %s
        ORDER BY kcu.ordinal_position
    """, (table_name,))

    keys = [row[0] for row in cursor.fetchall()]
    conn.close()
    return keys





def open_admin_crud():

    admin_window = tk.Toplevel(root)
    admin_window.title("Admin CRUD")
    admin_window.geometry("600x450")

    tables = [
        "applies_to",
        "category",
        "customer",
        "discount",
        "employee",
        "inventory",
        "inventory_audit_log",
        "location",
        "order_status_log",
        "orderitem",
        "orders",
        "product",
        "region",
        "store",
        "supplier"
    ]

    tk.Label(
        admin_window,
        text="Admin CRUD - All Tables",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    tk.Label(admin_window, text="Select Table").pack()

    table_combo = ttk.Combobox(
        admin_window,
        values=tables,
        state="readonly",
        width=35
    )
    table_combo.pack(pady=10)

    def selected_table():
        table = table_combo.get()

        if not table:
            messagebox.showerror("Error", "Please select a table")
            return None

        return table

    def view_table():
        table = selected_table()

        if table is None:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = sql.SQL("SELECT * FROM {} ORDER BY 1").format(
                sql.Identifier(table)
            )

            cursor.execute(query)

            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            conn.close()

            show_results(
                f"View Table - {table}",
                columns,
                rows
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_row():
        table = selected_table()

        if table is None:
            return

        columns = get_table_columns(table)
        primary_keys = get_primary_keys(table)

        add_window = tk.Toplevel(root)
        add_window.title(f"Add Row - {table}")
        add_window.geometry("500x600")

        entries = {}

        for col in columns:
            if len(primary_keys) == 1 and col == primary_keys[0]:
                continue

            tk.Label(add_window, text=col).pack()
            entry = tk.Entry(add_window, width=40)
            entry.pack(pady=3)
            entries[col] = entry

        def save_row():

            try:
                conn = get_connection()
                cursor = conn.cursor()

                insert_columns = list(entries.keys())
                values = []

                for col in insert_columns:
                    value = entries[col].get()

                    if value == "":
                        value = None

                    values.append(value)

                if len(primary_keys) == 1:
                    pk = primary_keys[0]

                    cursor.execute(
                        sql.SQL("SELECT COALESCE(MAX({}), 0) + 1 FROM {}").format(
                            sql.Identifier(pk),
                            sql.Identifier(table)
                        )
                    )

                    new_id = cursor.fetchone()[0]

                    insert_columns = [pk] + insert_columns
                    values = [new_id] + values

                query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                    sql.Identifier(table),
                    sql.SQL(", ").join(map(sql.Identifier, insert_columns)),
                    sql.SQL(", ").join(sql.Placeholder() * len(insert_columns))
                )

                cursor.execute(query, values)

                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Row added successfully")
                add_window.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(
            add_window,
            text="Save Row",
            command=save_row
        ).pack(pady=20)

    def update_row():
        table = selected_table()

        if table is None:
            return

        columns = get_table_columns(table)
        primary_keys = get_primary_keys(table)

        update_window = tk.Toplevel(root)
        update_window.title(f"Update Row - {table}")
        update_window.geometry("500x650")

        pk_entries = {}
        data_entries = {}

        tk.Label(
            update_window,
            text="Primary Key Values",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        for pk in primary_keys:

            tk.Label(update_window, text=pk).pack()

            # Product -> Combobox of all product IDs
            if table == "product" and pk == "productid":

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT productid
                    FROM product
                    ORDER BY productid
                """)

                product_ids = [
                    str(row[0])
                    for row in cursor.fetchall()
                ]

                conn.close()

                combo = ttk.Combobox(
                    update_window,
                    values=product_ids,
                    state="readonly",
                    width=37
                )

                combo.pack(pady=3)

                pk_entries[pk] = combo

            else:

                entry = tk.Entry(
                    update_window,
                    width=40
                )

                entry.pack(pady=3)

                pk_entries[pk] = entry

        tk.Label(
            update_window,
            text="Row Data",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        for col in columns:
            if col in primary_keys:
                continue

            tk.Label(update_window, text=col).pack()
            entry = tk.Entry(update_window, width=40)
            entry.pack(pady=3)
            data_entries[col] = entry

        def load_row():

            try:
                conn = get_connection()
                cursor = conn.cursor()

                where_clause = sql.SQL(" AND ").join(
                    sql.SQL("{} = %s").format(sql.Identifier(pk))
                    for pk in primary_keys
                )

                query = sql.SQL("SELECT * FROM {} WHERE {}").format(
                    sql.Identifier(table),
                    where_clause
                )

                pk_values = [
                    pk_entries[pk].get()
                    for pk in primary_keys
                ]

                cursor.execute(query, pk_values)

                row = cursor.fetchone()
                conn.close()

                if not row:
                    messagebox.showerror("Error", "Row not found")
                    return

                row_dict = dict(zip(columns, row))

                for col, entry in data_entries.items():
                    entry.delete(0, tk.END)

                    if row_dict[col] is not None:
                        entry.insert(0, row_dict[col])

            except Exception as e:
                messagebox.showerror("Error", str(e))

        def save_update():

            try:
                conn = get_connection()
                cursor = conn.cursor()

                set_clause = sql.SQL(", ").join(
                    sql.SQL("{} = %s").format(sql.Identifier(col))
                    for col in data_entries.keys()
                )

                where_clause = sql.SQL(" AND ").join(
                    sql.SQL("{} = %s").format(sql.Identifier(pk))
                    for pk in primary_keys
                )

                query = sql.SQL("UPDATE {} SET {} WHERE {}").format(
                    sql.Identifier(table),
                    set_clause,
                    where_clause
                )

                values = []

                for col in data_entries.keys():
                    value = data_entries[col].get()

                    if value == "":
                        value = None

                    values.append(value)

                for pk in primary_keys:
                    values.append(pk_entries[pk].get())

                cursor.execute(query, values)

                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Row updated successfully")
                update_window.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(
            update_window,
            text="Load Row",
            command=load_row
        ).pack(pady=10)

        tk.Button(
            update_window,
            text="Update Row",
            command=save_update
        ).pack(pady=10)

    def delete_row():
        table = selected_table()

        if table is None:
            return

        primary_keys = get_primary_keys(table)

        delete_window = tk.Toplevel(root)
        delete_window.title(f"Delete Row - {table}")
        delete_window.geometry("400x300")

        pk_entries = {}

        tk.Label(
            delete_window,
            text="Enter Primary Key Values",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        for pk in primary_keys:
            tk.Label(delete_window, text=pk).pack()
            entry = tk.Entry(delete_window, width=35)
            entry.pack(pady=3)
            pk_entries[pk] = entry

        def confirm_delete():

            try:
                conn = get_connection()
                cursor = conn.cursor()

                where_clause = sql.SQL(" AND ").join(
                    sql.SQL("{} = %s").format(sql.Identifier(pk))
                    for pk in primary_keys
                )

                query = sql.SQL("DELETE FROM {} WHERE {}").format(
                    sql.Identifier(table),
                    where_clause
                )

                values = [
                    pk_entries[pk].get()
                    for pk in primary_keys
                ]

                cursor.execute(query, values)

                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Row deleted successfully")
                delete_window.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(
            delete_window,
            text="Delete Row",
            command=confirm_delete
        ).pack(pady=20)

    tk.Button(
        admin_window,
        text="View Selected Table",
        width=30,
        command=view_table
    ).pack(pady=8)

    tk.Button(
        admin_window,
        text="Add Row",
        width=30,
        command=add_row
    ).pack(pady=8)

    tk.Button(
        admin_window,
        text="Update Row",
        width=30,
        command=update_row
    ).pack(pady=8)

    tk.Button(
        admin_window,
        text="Delete Row",
        width=30,
        command=delete_row
    ).pack(pady=8)

def run_low_stock_products():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("BEGIN;")
        cursor.execute("SELECT get_low_stock_products();")
        cursor.execute('FETCH ALL IN "low_stock_cursor";')

        rows = cursor.fetchall()

        conn.commit()
        conn.close()

        show_results(
            "Low Stock Products",
            ("Product ID", "Product Name", "Quantity", "Minimum Stock"),
            rows
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))
        
def open_queries():

    window = tk.Toplevel(root)

    window.title("Queries & Programs")
    window.geometry("550x450")

    tk.Label(
        window,
        text="Queries & Programs",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Button(
        window,
        text="Query 1 - Total Sales By Category",
        width=40,
        command=run_total_sales_by_category
    ).pack(pady=5)

    tk.Button(
        window,
        text="Query 2 - Expiring Products",
        width=40,
        command=run_expiring_products_query
    ).pack(pady=5)

    tk.Button(
        window,
        text="Function - Calculate Order Total",
        width=40,
        command=run_calculate_order_total
    ).pack(pady=5)
    
    tk.Button(
        window,
        text="Function - Low Stock Products",
        width=40,
        command=run_low_stock_products
    ).pack(pady=5)

    tk.Button(
        window,
        text="Procedure - Restock Inventory",
        width=40,
        command=run_restock_inventory
    ).pack(pady=5)

    tk.Button(
        window,
        text="Procedure - Update Expired Discounts",
        width=40,
        command=run_update_expired_discounts
    ).pack(pady=5)


# ==================================================
# Customer and Manager Panels
# ==================================================

def open_customer():

    window = tk.Toplevel(root)
    window.title("Customer")
    window.geometry("450x500")

    tk.Label(
        window,
        text="Customer Panel",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Button(
        window,
        text="Products",
        width=30,
        command=open_products_view
    ).pack(pady=5)

    tk.Button(
        window,
        text="Discounts",
        width=30,
        command=open_discounts
    ).pack(pady=5)

    tk.Button(
        window,
        text="Locations",
        width=30,
        command=open_locations
    ).pack(pady=5)

    tk.Button(
        window,
        text="Regions",
        width=30,
        command=open_regions
    ).pack(pady=5)

    tk.Button(
        window,
        text="Stores",
        width=30,
        command=open_stores
    ).pack(pady=5)

    tk.Button(
        window,
        text="Inventory",
        width=30,
        command=open_inventory
    ).pack(pady=5)


def open_manager():

    window = tk.Toplevel(root)
    window.title("Manager")
    window.geometry("500x600")

    tk.Label(
        window,
        text="Manager Panel",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Button(
        window,
        text="Database Connection Test",
        width=35,
        command=test_connection
    ).pack(pady=5)

    tk.Button(
        window,
        text="Queries & Programs",
        width=35,
        command=open_queries
    ).pack(pady=5)

    tk.Button(
        window,
        text="Inventory Audit Log",
        width=35,
        command=open_inventory_audit_log
    ).pack(pady=5)

    tk.Button(
        window,
        text="Order Status Log",
        width=35,
        command=open_order_status_log
    ).pack(pady=5)

    tk.Button(
        window,
        text="Admin CRUD",
        width=35,
        command=open_admin_crud
    ).pack(pady=5)


# ==================================================
# Main Window
# ==================================================

root = tk.Tk()
root.title("Rami Levy Online Database System")
root.state("zoomed")


try:
    bg_image = Image.open("screenshots/ramiPic.jpg")
    bg_image = bg_image.resize(
        (
            root.winfo_screenwidth(),
            root.winfo_screenheight()
        )
    )

    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

except Exception:
    root.configure(bg="#f5f5f5")

content_frame = tk.Frame(
    root,
    bg="#ffffff",
    bd=2,
    relief="ridge"
)

content_frame.place(
    relx=0.5,
    rely=0.35,
    anchor="center"
)

title = tk.Label(
    content_frame,
    text="Rami Levy Online",
    font=("Arial", 30, "bold"),
    bg="#ffffff"
)
title.pack(pady=20)


def add_main_button(text, command):
    tk.Button(
        content_frame,
        text=text,
        width=45,
        height=3,
        font=("Arial", 14, "bold"),
        command=command
    ).pack(pady=5)


add_main_button(
    "Customer",
    open_customer
)

add_main_button(
    "Manager",
    open_manager
)

add_main_button(
    "Exit",
    root.destroy
)

root.mainloop()