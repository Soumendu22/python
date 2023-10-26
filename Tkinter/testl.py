import tkinter as tk
from tkinter import ttk,messagebox
import sqlite3
import hashlib
import subprocess

class LoginGUI(tk.Tk):
    global self
    def __init__(self):
        
        super().__init__()

        self.title("User login")
        width=600
        height=400
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.config(bg='white')

        # Title Label
        title_lbl = tk.Label(self, text="Attendance Manager", font=("Arial", 18, "bold"), bg='white')
        title_lbl.pack(pady=10)

        # Username
        username_lbl = tk.Label(self, text="Username", font=("Arial", 15), bg='white')
        username_lbl.pack(pady=(0,5))

        global username_entry
        username_entry = tk.Entry(self, font=("Arial", 16), width=30, bd=2, relief='flat', fg='grey')
        username_entry.pack(pady=(0,20), ipady=2, padx=5)
        username_entry.config(highlightthickness=2, highlightbackground="grey")
        username_entry.insert(0, "Your username")
        username_entry.placeholder = "Your username"
        username_entry.bind("<FocusIn>", clear_placeholder)
        username_entry.bind("<FocusOut>", replace_placeholder)

        # Password
        password_lbl = tk.Label(self, text="Password", font=("Arial", 15), bg='white')
        password_lbl.pack(pady=(0,5))

        global password_entry
        password_entry = tk.Entry(self, font=("Arial", 16), width=30, show="", bd=2, relief='flat', fg='grey')
        password_entry.pack(pady=(0,20), ipady=1, padx=5)
        password_entry.config(highlightthickness=2, highlightbackground="grey")
        password_entry.insert(0, "Your Password")
        password_entry.placeholder = "Your Password"
        password_entry.bind("<FocusIn>", clear_placeholder)
        password_entry.bind("<FocusOut>", replace_placeholder)

        

        # Login in button
        login_button = tk.Button(self, text="Log in", font=("Arial", 16, "bold"), bg="black", fg="white", width=15, height=1, bd=0, relief='flat', command=login)
        login_button.pack(pady=8)

        # Login Button
        signup_btn = tk.Button(self, text="Don't have an account? Sign up", font=("Arial", 14), bg='white', relief='flat', bd=0, activebackground='white', foreground='blue', activeforeground='blue', cursor="hand2")
        signup_btn.pack(pady=10)
        def open_login_page(event):
            self.destroy()
            file_path = 'test.py'
            try:
                subprocess.Popen(['python', file_path])
            except FileNotFoundError:
                print("File not found.")
        signup_btn.bind("<Button-1>", open_login_page) 


def is_valid_email(email):
    # Check if the email contains "@" symbol
    return "@" in email

def login():
    username = username_entry.get()
    password = hashlib.sha256(password_entry.get().encode()).hexdigest()

    # Check if any of the fields are empty
    if not username or not password:
        messagebox.showinfo("All fields are required","Please fill all details")
        return

    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Welcome!!!","Login successfull")
        open_manager()
        self.destroy()
    else:
        messagebox.showinfo("Wrong Information","Invalid username or password")


def open_manager():
    file_path = 'home.py'
    try:
        subprocess.Popen(['python', file_path])
    except FileNotFoundError:
        print("File not found.")



def clear_placeholder(event):
    """Clear the placeholder text when entry is clicked."""
    if event.widget.get() == event.widget.placeholder:
        event.widget.delete(0, tk.END)
        event.widget.config(fg='black')
        if event.widget == password_entry:
            event.widget.config(show="•")

def replace_placeholder(event):
    """Replace the placeholder if the entry is empty."""
    if not event.widget.get():
        event.widget.config(fg='grey')
        event.widget.insert(0, event.widget.placeholder)
        if event.widget == password_entry:
            event.widget.config(show="")



app = LoginGUI()
app.mainloop()

