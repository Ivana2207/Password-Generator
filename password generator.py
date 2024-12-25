import tkinter as tk
import random
import sqlite3
from tkinter import messagebox

# Set up the SQLite database
conn = sqlite3.connect("data.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
)
""")
conn.commit()

def random_password():
    a = ['a', 'b', 'c', 'd', 'e']
    b = ['1', '2', '3', '4', '5']
    c = ['/', '@', '.', ',', '$']
    listi = a + b + c
    random.shuffle(listi)
    password = "".join(listi[:8])  # Combine the first 8 characters
    entry3.delete(0, tk.END)
    entry3.insert(0, password)

def add():
    text_web = entry1.get()
    text_email = entry2.get()
    text_pas = entry3.get()

    if text_email and text_web and text_pas:
        cursor.execute("INSERT INTO records (website, email, password) VALUES (?, ?, ?)",
                       (text_web, text_email, text_pas))
        conn.commit()

        entry1.delete(0, tk.END)
        entry2.delete(0, tk.END)
        entry3.delete(0, tk.END)
    else:
        messagebox.showinfo("Input Error", "Please fill in all fields before saving.")

def find():
    text_web = entry1.get().strip()
    if not text_web:
        messagebox.showinfo("Input Error", "Please enter a website to search for.")
        return

    cursor.execute("SELECT email, password FROM records WHERE LOWER(website) = LOWER(?)", (text_web,))
    result = cursor.fetchone()

    if result:
        email, password = result
        messagebox.showinfo("Found", f"Website: {text_web}\nEmail: {email}\nPassword: {password}")
    else:
        messagebox.showinfo("Not Found", "Website not found in the records.")

screen = tk.Tk()
screen.geometry("450x400")

canvas = tk.Canvas()
img = tk.PhotoImage(file="img.png")
canvas.config(width=200, height=200)
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)

# Create the UI elements
label1 = tk.Label(text="Website: ")
label1.grid(row=1, column=0)

entry1 = tk.Entry()
entry1.grid(row=1, column=1)

label2 = tk.Label(text="Email/Username: ")
label2.grid(row=2, column=0)

entry2 = tk.Entry()
entry2.grid(row=2, column=1)

label3 = tk.Label(text="Password: ")
label3.grid(row=3, column=0)

entry3 = tk.Entry()
entry3.grid(row=3, column=1)

button = tk.Button(text="Add", height=0, width=16, command=add)
button.grid(row=4, column=1)

button1 = tk.Button(text="Generate Password", width=16, command=random_password)
button1.grid(row=3, column=2)

button2 = tk.Button(text="Find", width=16, command=find)
button2.grid(row=2, column=2)

screen.mainloop()

# Close the database connection when the application closes
conn.close()
