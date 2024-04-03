import tkinter as tk
import cx_Oracle
import subprocess
import sys
from ingredients import update_ingredient_quantity

# Connect to Oracle Database
conn = cx_Oracle.connect(user="system", password="thing1318", dsn="XE", encoding="UTF-8")
cursor = conn.cursor()

def display_menu():
    menu_text.delete(1.0, tk.END)  # Clear previous menu display
    cursor.execute("SELECT item_name, price FROM menu")
    menu_text.insert(tk.END, "Menu:\n")
    for item_name, price in cursor:
        menu_text.insert(tk.END, f"{item_name} - ${price}\n")

def insert_order(c_id, item_id, quantity):
    # PL/SQL block to generate ORDER_ID
    plsql_block = """
        DECLARE
            l_order_id NUMBER;
        BEGIN
            SELECT order_id_sequence.NEXTVAL INTO l_order_id FROM dual;
            INSERT INTO orders (order_id, c_id, item_id, quantity) VALUES (l_order_id, :c_id, :item_id, :quantity);
            :order_id := l_order_id;
        END;
    """
    order_id = cursor.var(cx_Oracle.NUMBER)
    cursor.execute(plsql_block, {'c_id': c_id, 'item_id': item_id, 'quantity': quantity, 'order_id': order_id})
    conn.commit()
    result_label.config(text="Item added to order! Order ID: {}".format(order_id.getvalue()))



# Function to add an item to the order
def add_to_order(c_id):
    item_name = item_entry.get()
    quantity = int(quantity_entry.get())
    
    # Fetch item_id corresponding to the entered item_name
    cursor.execute("SELECT item_id FROM menu WHERE item_name = :item_name", {'item_name': item_name})
    row = cursor.fetchone()
    if row:
        item_id = row[0]
        insert_order(c_id, item_id, quantity)
        update_ingredient_quantity(item_id)  # Call the function to update ingredient quantity
    else:
        result_label.config(text="Invalid item name!")

# Function to handle payment
def pay_bill(c_id):
    # Call the next program to open the payment window
    subprocess.run(['python', 'C:/Users/Pratik Chakraborty/Documents/customer_pay_bill.py', str(c_id)])

# GUI Setup
root = tk.Tk()
root.title("Order Menu")

# Display Menu Button
display_menu_button = tk.Button(root, text="Display Menu", command=display_menu)
display_menu_button.pack()

menu_text = tk.Text(root, height=10, width=50)
menu_text.pack()

tk.Label(root, text="Select Item Name:").pack()
item_entry = tk.Entry(root)
item_entry.pack()

tk.Label(root, text="Enter Quantity:").pack()
quantity_entry = tk.Entry(root)
quantity_entry.pack()

# Ensure the previous window passes c_id as a command-line argument
c_id = sys.argv[1]

add_to_order_button = tk.Button(root, text="Add to Order", command=lambda: add_to_order(c_id))
add_to_order_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

# Button to indicate when the customer is done ordering items
pay_button = tk.Button(root, text="Pay Bill", command=lambda: pay_bill(c_id))
pay_button.pack()

root.mainloop()

# Close database connection
cursor.close()
conn.close()
