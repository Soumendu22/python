import tkinter as tk
from tkinter import ttk
import sqlite3
import hashlib
import subprocess

def login():
    username = username_entry.get()
    password = hashlib.sha256(password_entry.get().encode()).hexdigest()

    if not username or not password:
        status_label.config(text="All fields are required", foreground="red")
        return
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()

    if user:
        status_label.config(text="Login successful", foreground="green")
        open_manager()
        root.destroy()
    else:
        status_label.config(text="Invalid username or password", foreground="red")

def open_manager():
    file_path = 'manage.py'
    try:
        subprocess.Popen(['python', file_path])
    except FileNotFoundError:
        print("File not found.")

def open_signup_page(event):
    root.destroy()
    file_path = 'signup.py'
    try:
        subprocess.Popen(['python', file_path])
    except FileNotFoundError:
        print("File not found.")

def on_enter(event):
    style.map("TButton", background=[("active", "#001427")])

def on_leave(event):
    style.map("TButton", background=[("active", "#001427")])

root = tk.Tk()
root.title("User Login")
width=400
height=300
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)
style = ttk.Style()
style.configure("Custom.TButton", foreground="black", background="#390099", font=("Helvetica", 12))
style.configure("TLabel", font=("Helvetica", 12), background="#bbd0ff")
style.configure("TEntry", font=("Helvetica", 12))

username_label = ttk.Label(root, text="Username:")
username_label.pack(pady=10)
username_entry = ttk.Entry(root)
username_entry.pack(pady=5)

password_label = ttk.Label(root, text="Password:")
password_label.pack()
password_entry = ttk.Entry(root, show="*")
password_entry.pack(pady=5)

login_button = ttk.Button(root, text="Login", style="Custom.TButton", command=login)
login_button.pack(pady=10)
login_button.bind("<Enter>", on_enter)
login_button.bind("<Leave>", on_leave)

status_label = ttk.Label(root, text="", font=("Helvetica", 12))
status_label.pack()

login_label = tk.Label(root, text="Don't have an account? Signup", fg="blue", bg="#bbd0ff",cursor="hand2")
login_label.pack()
login_label.bind("<Button-1>", open_signup_page) 

root.configure(bg='#bbd0ff')
root.mainloop()
