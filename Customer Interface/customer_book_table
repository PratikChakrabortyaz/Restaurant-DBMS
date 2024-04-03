import tkinter as tk
import cx_Oracle
import subprocess
import sys
# Connect to Oracle Database
conn = cx_Oracle.connect(user="system", password="thing1318", dsn="XE", encoding="UTF-8")
cursor = conn.cursor()

def check_table_availability():
    table_availability = {}
    cursor.execute("SELECT table_no, availability FROM tables WHERE availability = 'Y'")
    for table_number, available in cursor:
        table_availability[table_number] = available
    return table_availability

def update_customer_table(c_id):
    table_number = table_entry.get()
    duration_minutes = int(duration_entry.get())
    
    cursor.execute("UPDATE customer SET table_no = :table_number, duration = :duration WHERE c_id = :c_id",
                   {'table_number': table_number, 'duration': duration_minutes, 'c_id': c_id})
    cursor.execute("UPDATE tables SET availability = 'N' WHERE table_no = :table_number", {'table_number': table_number})
    conn.commit()
    result_label.config(text="Table booking updated successfully!")
    
    # Call the order menu program with the same c_id
    subprocess.run(['python', 'C:/Users/Pratik Chakraborty/Documents/customer_order_menu.py', str(c_id)])

# Fetch table availability
table_availability = check_table_availability()

# GUI Setup
root = tk.Tk()
root.title("Table Booking")

tk.Label(root, text="Available Tables:").pack()
table_listbox = tk.Listbox(root)
for table_number, available in table_availability.items():
    table_listbox.insert(tk.END, f"Table {table_number}: {'Yes' if available == 'Y' else 'No'}")
table_listbox.pack()

tk.Label(root, text="Select Table Number:").pack()
table_entry = tk.Entry(root)
table_entry.pack()

tk.Label(root, text="Duration (minutes):").pack()
duration_entry = tk.Entry(root)
duration_entry.pack()

# Ensure the previous window passes c_id as a command-line argument
c_id = sys.argv[1]

submit_button = tk.Button(root, text="Submit Booking", command=lambda: update_customer_table(c_id))
submit_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()

# Close database connection
cursor.close()
conn.close()
