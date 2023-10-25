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

    conn = sqlite3.connect('faculty_database.db')
    cursor = conn.cursor()

     # Check if the username is already in use
    cursor.execute('SELECT username FROM faculty WHERE username = ?', (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        status_label.config(text="Username already exists", foreground="red")
    else:
        cursor.execute('INSERT INTO faculty (username, password, email) VALUES (?, ?, ?)', (username, password, email))
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

def open_login_page(event):
    root.destroy()
    file_path = 'loginfaculty.py'
    try:
        subprocess.Popen(['python', file_path])
    except FileNotFoundError:
        print("File not found.")

def on_enter(event):
    style.map("TButton", background=[("active", "#001427")])

def on_leave(event):
    style.map("TButton", background=[("active", "#001427")])


root = tk.Tk()
root.title("Faculty Signup")
width=400
height=300
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)
style = ttk.Style()
style.configure("Custom.TButton", foreground="black",background="#390099", font=("Helvetica", 12))
style.configure("TLabel", font=("Helvetica", 12), background="#bbd0ff")
style.configure("TEntry", font=("Helvetica", 15))

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

signup_button = ttk.Button(root, text="Signup", cursor="hand2",style="Custom.TButton", command=signup)
signup_button.pack(pady=10)
signup_button.bind("<Enter>", on_enter)
signup_button.bind("<Leave>", on_leave)

status_label = ttk.Label(root, text="", font=("Helvetica", 12))
status_label.pack()

login_label = tk.Label(root, text="Already have an account? Login", fg="blue", bg="#bbd0ff",cursor="hand2")
login_label.pack()
login_label.bind("<Button-1>", open_login_page) 

root.configure(bg='#bbd0ff')
root.mainloop()
