import tkinter as tk
import cx_Oracle
import subprocess

# Connect to Oracle Database
conn = cx_Oracle.connect(user="system", password="thing1318", dsn="XE", encoding="UTF-8")
cursor = conn.cursor()

def insert_customer():
    name = name_entry.get()
    phone_number = phone_entry.get()
    
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
    subprocess.run(['python', 'C:/Users/Pratik Chakraborty/Documents/customer_book_table.py', str(c_id.getvalue())])

# GUI Setup for Customer Registration
root = tk.Tk()
root.title("Customer Registration")

# Customer Registration Widgets
tk.Label(root, text="Name:").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Phone Number:").pack()
phone_entry = tk.Entry(root)
phone_entry.pack()

insert_button = tk.Button(root, text="Register", command=insert_customer)
insert_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

# Run main event loop
root.mainloop()

# Close database connection
cursor.close()
conn.close()
