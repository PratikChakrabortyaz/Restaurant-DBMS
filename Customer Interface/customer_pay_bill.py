import tkinter as tk
import cx_Oracle
import sys
import subprocess

# Connect to Oracle Database
conn = cx_Oracle.connect(user="system", password="thing1318", dsn="XE", encoding="UTF-8")
cursor = conn.cursor()

def generate_bill(c_id):
    cursor.execute("""
        SELECT o.order_id, m.item_name, o.quantity, m.price * o.quantity AS item_total
        FROM orders o
        JOIN menu m ON o.item_id = m.item_id
        WHERE o.c_id = :c_id
    """, {'c_id': c_id})
    bill_text.delete(1.0, tk.END)  # Clear previous bill display
    total_price = 0
    for order_id, item_name, quantity, item_total in cursor:
        total_price += item_total
        bill_text.insert(tk.END, f"Order ID: {order_id}, Item: {item_name}, Quantity: {quantity}, Item Total: ${item_total:.2f}\n")
    discount_percentage = get_discount_percentage(total_price)
    discount = total_price * discount_percentage 
    total_price_after_discount = total_price - discount
    bill_text.insert(tk.END, f"\nTotal Price: ${total_price:.2f}\nDiscount Percentage: {discount_percentage*100}%\nDiscount Applied: ${discount:.2f}\nTotal Price after Discount: ${total_price_after_discount:.2f}\n")
    insert_bill(total_price_after_discount, c_id)
    give_rating_button = tk.Button(root, text="Give Rating", command=lambda: give_rating(c_id))
    give_rating_button.pack()

def insert_bill(total_price_after_discount, c_id):
    discount_id = get_discount_id(total_price_after_discount)
    plsql_block = """
        DECLARE
            l_bill_id NUMBER;
        BEGIN
            SELECT bill_id_sequence.NEXTVAL INTO l_bill_id FROM dual;
            INSERT INTO bill (bill_id, c_id, amount, disc_id)
            VALUES (l_bill_id, :c_id, :amount, :disc_id);
            COMMIT;
        END;
    """
    cursor.execute(plsql_block, {'c_id': c_id, 'amount': total_price_after_discount, 'disc_id': discount_id})
    conn.commit()

def get_discount_percentage(total_price):
    cursor.execute("""
        SELECT PERCENTAGE
        FROM discount_policy
        WHERE (:total_price >= 5 AND :total_price < 10 AND disc_id = 1)
        OR (:total_price >= 10 AND :total_price < 15 AND disc_id = 2)
        OR (:total_price >= 15 AND disc_id = 3)
    """, {'total_price': total_price})
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        return 0

def get_discount_id(total_price_after_discount):
    if total_price_after_discount >= 5 and total_price_after_discount < 10:
        return 1
    elif total_price_after_discount >= 10 and total_price_after_discount < 15:
        return 2
    elif total_price_after_discount >= 15:
        return 3
    else:
        return None

def give_rating(c_id):
    subprocess.run(['python', 'C:/Users/Pratik Chakraborty/Documents/customer_gives_rating.py', str(c_id)])

# GUI Setup
root = tk.Tk()
root.title("Bill Payment")

c_id = sys.argv[1]

generate_bill_button = tk.Button(root, text="Generate Bill", command=lambda: generate_bill(c_id))
generate_bill_button.pack()

bill_text = tk.Text(root, height=15, width=50)
bill_text.pack()

root.mainloop()

# Close database connection
cursor.close()
conn.close()
