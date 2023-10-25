import tkinter as tk
from tkinter import ttk
import sqlite3
import hashlib

def login():
    username = username_entry.get()
    password = hashlib.sha256(password_entry.get().encode()).hexdigest()

    if not username or not password:
        status_label.config(text="Both username and password are required", foreground="red")
        return  # Exit the function if any field is empty

    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()

    if user:
        status_label.config(text="Login successful", foreground="green")
        open_dashboard()
        root1.destroy()
    else:
        status_label.config(text="Invalid username or password", foreground="red")

def open_dashboard():
    dashboard_window = tk.Toplevel(root1)
    dashboard_window.title("Dashboard")

    dashboard_label = ttk.Label(dashboard_window, text="Welcome to the Dashboard", font=("Helvetica", 16))
    dashboard_label.pack(pady=20)

root1 = tk.Tk()
root1.title("User Login")

style = ttk.Style()
style.configure("TButton", background="#4CAF50", font=("Helvetica", 12))
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12))

username_label = ttk.Label(root1, text="Username*:")  # Marked as required with an asterisk
username_label.grid(row=0, column=0, pady=10)
username_entry = ttk.Entry(root1)
username_entry.grid(row=0, column=1, pady=5)

password_label = ttk.Label(root1, text="Password*:")  # Marked as required with an asterisk
password_label.grid(row=1, column=0)
password_entry = ttk.Entry(root1, show="*")
password_entry.grid(row=1, column=1, pady=5)

login_button = ttk.Button(root1, text="Login", command=login)
login_button.grid(row=2, column=1, pady=10)

status_label = ttk.Label(root1, text="", font=("Helvetica", 12))
status_label.grid(row=3, columnspan=2)

root1.geometry("400x300")
root1.configure(bg='#ECECEC')
root1.mainloop()
