import tkinter as tk
from tkinter import ttk
import sqlite3
import hashlib
import subprocess

def is_valid_email(email):
    # Check if the email contains "@" symbol
    return "@" in email

def signup():
    username = username_entry.get()
    password = hashlib.sha256(password_entry.get().encode()).hexdigest()
    email = email_entry.get()

    # Check if any of the fields are empty
    if not username or not password or not email:
        status_label.config(text="All fields are required", foreground="red")
        return
    if not is_valid_email(email):
        status_label.config(text="Invalid email format (missing @ symbol)", foreground="red")
        return

    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

     # Check if the username is already in use
    cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        status_label.config(text="Username already exists", foreground="red")
    else:
        cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, password, email))
        conn.commit()
        conn.close()
        status_label.config(text="Signup successful", foreground="green")
        open_manager()
        root.destroy()
def open_manager():
    file_path = 'home.py'
    try:
        subprocess.Popen(['python', file_path])
    except FileNotFoundError:
        print("File not found.")

root = tk.Tk()
root.title("User Signup")
width=400
height=300
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)
style = ttk.Style()
style.configure("TButton", foreground="black",background="#000000", font=("Helvetica", 12))
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12))

username_label = ttk.Label(root, text="Username:")
username_label.pack(pady=10)
username_entry = ttk.Entry(root)
username_entry.pack(pady=5)

password_label = ttk.Label(root, text="Password:")
password_label.pack()
password_entry = ttk.Entry(root, show="*")
password_entry.pack(pady=5)

email_label = ttk.Label(root, text="Email:")
email_label.pack()
email_entry = ttk.Entry(root)
email_entry.pack(pady=5)

signup_button = ttk.Button(root, text="Signup", command=signup)
signup_button.pack(pady=10)

status_label = ttk.Label(root, text="", font=("Helvetica", 12))
status_label.pack()

root.configure(bg='#ECECEC')
root.mainloop()
