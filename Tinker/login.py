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
    file_path = 'aaa.py'
    try:
                subprocess.Popen(['python', file_path])
    except FileNotFoundError:
                print("File not found.")
root = tk.Tk()
root.title("User Login")
width=450
height=250
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)
style = ttk.Style()
style.configure("TButton", foreground="black", background="#000000", font=("Helvetica", 12))
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

login_button = ttk.Button(root, text="Login", command=login)
login_button.pack(pady=10)

status_label = ttk.Label(root, text="", font=("Helvetica", 12))
status_label.pack()

root.geometry("400x300")
root.configure(bg='#ECECEC')
root.mainloop()
