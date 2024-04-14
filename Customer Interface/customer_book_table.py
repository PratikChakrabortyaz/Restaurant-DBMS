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
    
    # Check if the table exists in the tables list
    cursor.execute("SELECT availability FROM tables WHERE table_no = :table_number", {'table_number': table_number})
    row = cursor.fetchone()
    if row is None:
        result_label.config(text=f"Table {table_number} does not exist", fg="red")
        return
    
    availability = row[0]
    
    # Check if the table is available
    if availability == 'N':
        result_label.config(text=f"Table {table_number} is not available", fg="red")
        return
    
    # Update the customer's table and set its availability to 'N'
    cursor.execute("UPDATE customer SET table_no = :table_number, duration = :duration WHERE c_id = :c_id",
                   {'table_number': table_number, 'duration': duration_minutes, 'c_id': c_id})
    cursor.execute("UPDATE tables SET availability = 'N' WHERE table_no = :table_number", {'table_number': table_number})
    conn.commit()
    result_label.config(text="Table booking updated successfully!")
    
    # Call the order menu program with the same c_id
    root.destroy()
    subprocess.run(['python', 'C:/Users/Pratik Chakraborty/Documents/customer_order_menu.py', str(c_id)])
    



# Fetch table availability
table_availability = check_table_availability()

# GUI Setup
root = tk.Tk()
root.title("Table Booking")

# Set window dimensions
window_width = root.winfo_screenwidth() // 2
window_height = root.winfo_screenheight() // 2
root.geometry(f"{window_width}x{window_height}")

# Styling
root.configure(bg="#3E4095")  # French flag blue background

# Table numbers display
table_numbers_frame = tk.Frame(root, bg="#E4E4E4")  # White background
table_numbers_frame.pack()

for table_number, available in table_availability.items():
    table_label = tk.Label(table_numbers_frame, text=f"Table {table_number}", bg="#FFD700", font=("Helvetica", 14, "bold"), padx=10, pady=5, fg="#3E4095")  # Gold text on blue background
    table_label.grid(row=0, column=table_number-1)

# Label and Entry for table number selection
table_entry_label = tk.Label(root, text="Select Table Number:", bg="#3E4095", fg="white", font=("Helvetica", 12, "bold"))
table_entry_label.pack()
table_entry = tk.Entry(root, bg="#FFD700", fg="black", font=("Helvetica", 10))  # Gold text on blue background
table_entry.pack()

# Label and Entry for duration input
duration_label = tk.Label(root, text="Duration (minutes):", bg="#3E4095", fg="white", font=("Helvetica", 12, "bold"))
duration_label.pack()
duration_entry = tk.Entry(root, bg="#FFD700", fg="black", font=("Helvetica", 10))  # Gold text on blue background
duration_entry.pack()

# Ensure the previous window passes c_id as a command-line argument
c_id = sys.argv[1]

# Submit button
submit_button = tk.Button(root, text="Submit Booking", command=lambda: update_customer_table(c_id), bg="#FF0000", fg="white", font=("Helvetica", 12, "bold"))  # Red button
submit_button.pack()

# Result label
result_label = tk.Label(root, text="", bg="#3E4095", fg="red", font=("Helvetica", 10))  # Red text on blue background
result_label.pack()

root.mainloop()

# Close database connection
cursor.close()
conn.close()
