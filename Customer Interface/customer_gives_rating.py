import tkinter as tk
import cx_Oracle
import sys


# Connect to Oracle Database
conn = cx_Oracle.connect(user="system", password="thing1318", dsn="XE", encoding="UTF-8")
cursor = conn.cursor()

def submit_review(c_id):
    rating = rating_var.get()
    review_text = review_entry.get("1.0", tk.END).strip()
    if rating and review_text:
        gives_id = cursor.var(cx_Oracle.NUMBER)
        cursor.execute("""
            INSERT INTO gives (gives_id, c_id, rating, review) 
            VALUES (gives_id_sequence.NEXTVAL, :c_id, :rating, :review_text) 
            RETURNING gives_id INTO :gives_id
        """, {'c_id': c_id, 'rating': rating, 'review_text': review_text, 'gives_id': gives_id})
        conn.commit()
        gives_id = gives_id.getvalue()
        if gives_id:
            result_label.config(text="Review submitted successfully!")
        else:
            result_label.config(text="Error submitting review!")
    else:
        result_label.config(text="Please provide a rating and review.")

# GUI Setup
root = tk.Tk()
root.title("Customer Review")

rating_var = tk.StringVar()
rating_label = tk.Label(root, text="Rating (1-5):")
rating_label.pack()

# Create buttons for rating selection
for i in range(1, 6):
    rating_button = tk.Radiobutton(root, text=str(i), variable=rating_var, value=i)
    rating_button.pack()

review_label = tk.Label(root, text="Review:")
review_label.pack()
review_entry = tk.Text(root, height=5, width=50)
review_entry.pack()
c_id = sys.argv[1]

submit_review_button = tk.Button(root, text="Submit Review", command=lambda: submit_review(c_id))
submit_review_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()

# Close database connection
cursor.close()
conn.close()
