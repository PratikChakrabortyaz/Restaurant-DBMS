import tkinter as tk
import cx_Oracle

# Connect to Oracle Database
conn = cx_Oracle.connect(user="system", password="thing1318", dsn="XE", encoding="UTF-8")
cursor = conn.cursor()

def total_revenue_generated():
    total_revenue = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("calculate_total_revenue", (total_revenue,))
    result_label.config(text=f"Total revenue generated: {total_revenue.getvalue()}")

# Function to display text fields for updating menu items
def display_update_menu_item_fields():
    item_name_label.pack()
    item_name_entry.pack()
    price_label.pack()
    price_entry.pack()
    update_menu_item_button.pack()

# Function to update menu items
def update_menu_item():
    item_name = item_name_entry.get()
    price = price_entry.get()
    try:
        price = float(price)
        cursor.execute("UPDATE menu SET price = :price WHERE item_name = :item_name", {'price': price, 'item_name': item_name})
        conn.commit()
        result_label.config(text="Menu item updated successfully!")
    except ValueError:
        result_label.config(text="Invalid price! Please enter a valid number.")

# Function to display the most ordered item in menu
def most_ordered_item():
    cursor.execute("""
        WITH OrderSummary AS (
            SELECT item_id, SUM(quantity) AS total_quantity
            FROM orders
            GROUP BY item_id
        )
        SELECT m.item_name, os.total_quantity
        FROM OrderSummary os
        JOIN menu m ON os.item_id = m.item_id
        WHERE total_quantity = (SELECT MAX(total_quantity) FROM OrderSummary)
    """)
    row = cursor.fetchone()
    if row:
        result_label.config(text=f"Most ordered item: {row[0]}, Total Quantity: {row[1]}")
    else:
        result_label.config(text="No orders yet!")

# Function to create and display the view
def create_and_display_view():
    try:
        cursor.execute("DROP VIEW customer_order_view")
        conn.commit()
        result_label.config(text="Existing view dropped successfully!")
    except cx_Oracle.DatabaseError as e:
        # If the view does not exist or there's an error dropping it, ignore and continue
        pass
    
    cursor.execute("""
        CREATE VIEW customer_order_view AS
        SELECT c.name, c.table_no, m.item_name,r.rating
        FROM customer c
        LEFT JOIN orders o ON c.c_id = o.c_id
        LEFT JOIN menu m ON o.item_id = m.item_id
        LEFT JOIN gives g ON c.c_id = g.c_id
        LEFT JOIN rating r ON g.r_id = r.r_id
    """)
    conn.commit()
    result_label.config(text="View created successfully!")
    display_view()


def display_view():
    cursor.execute("""
        SELECT name, table_no, item_name, rating
        FROM customer_order_view
    """)
    rows = cursor.fetchall()
    
    # Clear existing content
    view_text.delete(1.0, tk.END)
    
    # Add headings
    headings = ["Customer Name", "Table No", "Item Ordered", "Rating Given"]
    view_text.insert(tk.END, " | ".join(headings) + "\n")
    view_text.insert(tk.END, "-" * (len(" | ".join(headings))) + "\n")
    
    # Add rows
    for row in rows:
        view_text.insert(tk.END, " | ".join(str(value) for value in row) + "\n")




# GUI Setup
root = tk.Tk()
root.title("Restaurant Side Interface")

# Entry widgets for user input
item_name_label = tk.Label(root, text="Item Name:")
item_name_entry = tk.Entry(root)

price_label = tk.Label(root, text="Price:")
price_entry = tk.Entry(root)

# Main menu buttons
total_revenue_button = tk.Button(root, text="Total Revenue Generated", command=total_revenue_generated)
total_revenue_button.pack()

update_menu_item_button = tk.Button(root, text="Update Menu Item", command=display_update_menu_item_fields)
update_menu_item_button.pack()

most_ordered_item_button = tk.Button(root, text="Most Ordered Item in Menu", command=most_ordered_item)
most_ordered_item_button.pack()

create_view_button = tk.Button(root, text="Create and Display View", command=create_and_display_view)
create_view_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

view_text = tk.Text(root, height=20, width=70)
view_text.pack()

root.mainloop()

# Close database connection
cursor.close()
conn.close()
