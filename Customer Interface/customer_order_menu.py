import tkinter as tk
import cx_Oracle
import subprocess
import sys

# Connect to Oracle Database
conn = cx_Oracle.connect(user="system", password="thing1318", dsn="XE", encoding="UTF-8")
cursor = conn.cursor()

def display_menu():
    menu_text.delete(1.0, tk.END)  # Clear previous menu display
    cursor.execute("SELECT item_name, price FROM menu")
    menu_text.insert(tk.END, "Menu:\n")
    for item_name, price in cursor:
        menu_text.insert(tk.END, f"{item_name} - ${price}\n")
    # Update text appearance
    menu_text.config(bg="#F0F8FF", fg="#4682B4", font=("Helvetica", 12, "bold"))  # Alice blue background, steel blue text color

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
        result_label.config(text="Item added to order!")
    else:
        result_label.config(text="Invalid item name!")

# Function to handle payment
def pay_bill(c_id):
    # Call the next program to open the payment window
    root.destroy()
    subprocess.run(['python', 'C:/Users/Pratik Chakraborty/Documents/customer_pay_bill.py', str(c_id)])
    

# GUI Setup
root = tk.Tk()
root.title("Order Menu")

# Set window dimensions
window_width = root.winfo_screenwidth() // 2
window_height = root.winfo_screenheight() // 2
root.geometry(f"{window_width}x{window_height}")

# Styling
root.configure(bg="#FFF5EE")  # French vanilla background color

# Display Menu Button
display_menu_button = tk.Button(root, text="Display Menu", command=display_menu, bg="#4682B4", fg="white")  # Steel blue button
display_menu_button.pack()

menu_text = tk.Text(root, height=10, width=50)
menu_text.pack()

tk.Label(root, text="Select Item Name:", bg="#FFF5EE").pack()
item_entry = tk.Entry(root, bg="#F0E68C")  # Khaki entry field
item_entry.pack()

tk.Label(root, text="Enter Quantity:", bg="#FFF5EE").pack()
quantity_entry = tk.Entry(root, bg="#F0E68C")  # Khaki entry field
quantity_entry.pack()

# Ensure the previous window passes c_id as a command-line argument
c_id = sys.argv[1]

add_to_order_button = tk.Button(root, text="Add to Order", command=lambda: add_to_order(c_id), bg="#4682B4", fg="white")  # Steel blue button
add_to_order_button.pack()

result_label = tk.Label(root, text="", bg="#FFF5EE", fg="red")  # Red text on French vanilla background
result_label.pack()

# Button to indicate when the customer is done ordering items
pay_button = tk.Button(root, text="Pay Bill", command=lambda: pay_bill(c_id), bg="#4682B4", fg="white")  # Steel blue button
pay_button.pack()

root.mainloop()

# Close database connection
cursor.close()
conn.close()
