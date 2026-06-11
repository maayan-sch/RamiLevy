import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from db_config import get_connection
from PIL import Image, ImageTk


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
                p.brand
            FROM product p
            JOIN category c
                ON p.categoryid = c.categoryid
            JOIN supplier s
                ON p.supplierid = s.supplierid
            ORDER BY p.productid
            LIMIT 100
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
                "Brand"
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
                    row[5]
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
            p.brand
        FROM product p
        JOIN category c
            ON p.categoryid = c.categoryid
        JOIN supplier s
            ON p.supplierid = s.supplierid
        ORDER BY p.productid DESC
        LIMIT 100
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
                row[5]
            )
        )

    conn.close()

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
    result_window.geometry("900x500")

    tk.Label(
        result_window,
        text=title,
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    tree = ttk.Treeview(
        result_window,
        columns=columns,
        show="headings"
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    for row in rows:
        tree.insert("", tk.END, values=row)

    tree.pack(fill="both", expand=True, padx=10, pady=10)


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
            WHERE p.expirationdate <= CURRENT_DATE + INTERVAL '30 days'
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
                phone
            FROM customer
            ORDER BY customername
        """)

        rows = cursor.fetchall()
        conn.close()

        show_results(
            "Customers",
            ("Customer Name", "Email", "Phone"),
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
                o.orderstatus
            FROM orders o
            JOIN customer c
                ON o.customerid = c.customerid
            ORDER BY o.orderdate DESC
            LIMIT 100
        """)

        rows = cursor.fetchall()
        conn.close()

        show_results(
            "Orders",
            ("Customer", "Order Date", "Total Amount", "Status"),
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
                o.orderid,
                p.productname,
                oi.quantity,
                oi.subtotal,
                oi.inonsale,
                oi.saledescription
            FROM orderitem oi
            JOIN product p
                ON oi.productid = p.productid
            JOIN orders o
                ON oi.orderid = o.orderid
            ORDER BY o.orderid DESC
            LIMIT 100
        """)

        rows = cursor.fetchall()
        conn.close()

        show_results(
            "Order Items",
            (
                "Order",
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
            LIMIT 100
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
                productid,
                oldquantity,
                newquantity,
                changedate
            FROM inventory_audit_log
            ORDER BY logid DESC
            LIMIT 100
        """)

        rows = cursor.fetchall()
        conn.close()

        show_results(
            "Inventory Audit Log",
            (
                "Product ID",
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
                orderid,
                oldstatus,
                newstatus,
                changedate
            FROM order_status_log
            ORDER BY logid DESC
            LIMIT 100
        """)

        rows = cursor.fetchall()
        conn.close()

        show_results(
            "Order Status Log",
            (
                "Order ID",
                "Old Status",
                "New Status",
                "Change Date"
            ),
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
# Main Window
# ==================================================

root = tk.Tk()
root.title("Rami Levy Online Database System")
root.geometry("750x750")

canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
def center_frame(event):
    canvas.itemconfig(
        canvas_window,
        width=event.width
    )

canvas.bind("<Configure>", center_frame)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

try:
    bg_image = Image.open("screenshots/ramiPic.jpg")
    bg_image = bg_image.resize((750, 1000))
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(scrollable_frame, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

except Exception:
    scrollable_frame.configure(bg="#f5f5f5")

content_frame = tk.Frame(scrollable_frame, bg="#ffffff", bd=2, relief="ridge")
content_frame.pack(pady=30)

title = tk.Label(
    content_frame,
    text="Rami Levy Online\nDatabase Management System",
    font=("Arial", 20, "bold"),
    bg="#ffffff"
)
title.pack(pady=20)


def add_main_button(text, command):
    tk.Button(
        content_frame,
        text=text,
        width=35,
        height=2,
        command=command
    ).pack(pady=5)


add_main_button("Test Database Connection", test_connection)
add_main_button("Products", open_products)
add_main_button("Suppliers", open_suppliers)
add_main_button("Customers", open_customers)
add_main_button("Inventory", open_inventory)
add_main_button("Inventory Audit Log", open_inventory_audit_log)
add_main_button("Order Status Log", open_order_status_log)
add_main_button("Orders", open_orders)
add_main_button("Categories", open_categories)
add_main_button("Discounts", open_discounts)
add_main_button("Employees", open_employees)
add_main_button("Locations", open_locations)
add_main_button("Regions", open_regions)
add_main_button("Order Items", open_order_items)
add_main_button("Product Discounts", open_applies_to)
add_main_button("Stores", open_stores)
add_main_button("Queries & Programs", open_queries)
add_main_button("Exit", root.destroy)

root.mainloop()