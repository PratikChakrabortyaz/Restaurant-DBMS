import tkinter as tk
import cx_Oracle
import sys

# Connect to Oracle Database
conn = cx_Oracle.connect(user="system", password="thing1318", dsn="XE", encoding="UTF-8")
cursor = conn.cursor()

def submit_review(c_id):
    rating = rating_var.get()
    review_text = review_entry.get("1.0", tk.END).strip()
    if rating or review_text:
        # Insert into rating table
        cursor.execute("""
            INSERT INTO rating (r_id, rating, review) 
            VALUES (rating_id_sequence.NEXTVAL, :rating, :review_text)
        """, {'rating': rating, 'review_text': review_text})
        conn.commit()

        # Get the last inserted r_id
        cursor.execute("SELECT MAX(r_id) FROM rating")
        r_id = cursor.fetchone()[0]

        # Insert into gives table
        cursor.execute("""
            INSERT INTO gives (c_id, r_id) 
            VALUES (:c_id, :r_id)
        """, {'c_id': c_id, 'r_id': r_id})
        conn.commit()

        result_label.config(text="Review submitted successfully!", fg="#008000")
        
        show_thank_you_window()
        
    else:
        result_label.config(text="Review submitted without rating or review.", fg="#FF0000")
        show_thank_you_window()
        

def show_thank_you_window():
    # Create a new window for thank you message
    thank_you_window = tk.Toplevel(root)
    thank_you_window.title("Thank You!")

    # Create a colorful heading
    heading_label = tk.Label(thank_you_window, text="Thank you for dining in French Restaurant.\nPlease visit again!", font=("Arial", 16), fg="#003399")
    heading_label.pack(padx=20, pady=20)

    # Adjust window size
    thank_you_window.geometry("400x200")

# GUI Setup
root = tk.Tk()
root.title("Customer Review")

root.configure(bg="#F4E1D2")  # Set background color

rating_var = tk.StringVar(value="")
rating_label = tk.Label(root, text="Rating (1-5):", bg="#F4E1D2", fg="#003399", font=("Arial", 14, "bold"))
rating_label.pack()

# Create buttons for rating selection
rating_buttons = []
for i in range(1, 6):
    rating_button = tk.Radiobutton(root, text=str(i), variable=rating_var, value=str(i), bg="#F4E1D2", font=("Arial", 12), indicatoron=0)
    rating_button.pack(pady=5)
    rating_buttons.append(rating_button)

review_label = tk.Label(root, text="Review:", bg="#F4E1D2", fg="#003399", font=("Arial", 14, "bold"))
review_label.pack()

review_entry = tk.Text(root, height=5, width=50, bg="#FFEBCD", fg="#000000", font=("Arial", 12))
review_entry.pack()

c_id = sys.argv[1]

submit_review_button = tk.Button(root, text="Submit Review", command=lambda: submit_review(c_id), bg="#003399", fg="#FFFFFF", font=("Arial", 14, "bold"))
submit_review_button.pack(pady=10)

result_label = tk.Label(root, text="", bg="#F4E1D2", fg="#FF0000", font=("Arial", 12))
result_label.pack()

root.mainloop()

# Close database connection
cursor.close()
conn.close()
