import tkinter as tk
import cx_Oracle
import subprocess

# Connect to Oracle Database
conn = cx_Oracle.connect(user="system", password="thing1318", dsn="XE", encoding="UTF-8")
cursor = conn.cursor()

def insert_customer():
    name = name_entry.get()
    phone_number = phone_entry.get()
    
    # Check phone number length using SQL function
    cursor.execute("SELECT LENGTH(:phone_number) FROM dual", {'phone_number': phone_number})
    phone_length = cursor.fetchone()[0]
    
    if phone_length != 10:
        result_label.config(text="The phone number must have 10 digits", fg="red")
    else:
        # PL/SQL block to generate c_id and insert data
        plsql_block = """
            DECLARE
                l_id NUMBER;
            BEGIN
                SELECT customer_seq.NEXTVAL INTO l_id FROM dual;
                INSERT INTO customer (c_id, name, phone_number) VALUES (l_id, :name, :phone_number);
                :c_id := l_id;
            END;
        """
        c_id = cursor.var(cx_Oracle.NUMBER)
        cursor.execute(plsql_block, {'name': name, 'phone_number': phone_number, 'c_id': c_id})
        conn.commit()
        
        # Call the next program to open the table booking window
        root.destroy()
        subprocess.run(['python', 'C:/Users/Pratik Chakraborty/Documents/customer_book_table.py', str(c_id.getvalue())])
        

# GUI Setup for Customer Registration
root = tk.Tk()
root.title("Customer Registration")

# Set window icon (French flag)
icon = tk.PhotoImage(file="C:/Users/Pratik Chakraborty/Documents/french_flag.png")
root.iconphoto(True, icon)

# Set background color
root.configure(bg="#E7EFF6")  # Light blue color

# Heading
heading_label = tk.Label(root, text="Bienvenue au Restaurant Français", font=("Helvetica", 18, "bold"), bg="#E7EFF6", fg="#FF0000")
heading_label.pack(pady=10)

# Mini Heading
subheading_label = tk.Label(root, text="Enter your details", font=("Helvetica", 14), bg="#E7EFF6", fg="#FF0000")
subheading_label.pack()

# Customer Registration Widgets
tk.Label(root, text="Name:", bg="#E7EFF6", fg="#FF0000").pack()
name_entry = tk.Entry(root, bg="white", fg="black", font=("Helvetica", 12))
name_entry.pack()

tk.Label(root, text="Phone Number:", bg="#E7EFF6", fg="#FF0000").pack()
phone_entry = tk.Entry(root, bg="white", fg="black", font=("Helvetica", 12))
phone_entry.pack()

insert_button = tk.Button(root, text="Register", command=insert_customer, bg="#FF0000", fg="white", font=("Helvetica", 12, "bold"))
insert_button.pack(pady=10)

result_label = tk.Label(root, text="", bg="#E7EFF6", fg="#FF0000")
result_label.pack()

# Run main event loop
root.mainloop()

# Close database connection
cursor.close()
conn.close()
