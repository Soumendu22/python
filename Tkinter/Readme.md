# - ----------------Database
import sqlite3 as sql
def createusers():
    conn =sql.connect('attendance.db')
    c=conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Users(
        	id INTEGER NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
	        password	TEXT NOT NULL,
	        email	TEXT NOT NULL UNIQUE,
	        PRIMARY KEY(id AUTOINCREMENT))''')
    conn.commit()
    conn.close()
    
def createattable():
    conn =sql.connect('attendance.db')
    c=conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attable(
        	subid INTEGER NOT NULL,
            subject TEXT NOT NULL UNIQUE,
	        attended INT ,
	        bunked INT ,
            percentage DECIMAL(4,2),
            id INT NOT NULL,
            FOREIGN KEY(id) REFERENCES Users(id),
	        PRIMARY KEY(subid AUTOINCREMENT))''')
    conn.commit()
    conn.close()

def adduser(username, password, email):
    user = username
    passw = password
    e_mail = email
    conn = sql.connect('attendance.db')
    c = conn.cursor()
    c.execute('''INSERT INTO Users (username, password,email) VALUES (?,?,?)''',(user, passw, e_mail))
    conn.commit()
    conn.close()   

def addattendance(subject, attended, bunked, percentage,id):
    sname = subject
    std = attended
    sbunk = bunked
    spercent = percentage
    uid = id
    conn = sql.connect('attendance.db')
    c = conn.cursor()
    c.execute('''INSERT INTO attable (subject, attended, bunked, percentage,id) VALUES (?, ?, ?, ?,?)''', (sname,std, sbunk, spercent,uid))
    conn.commit()
    conn.close()
    

def attendmanage(subid, attend, bunk, percent):
    attended = attend
    bunked = bunk
    percentage = percent
    conn = sql.connect('attendance.db')
    c = conn.cursor()
    c.execute(''' UPDATE attable SET attended=?, bunked=?, percentage=? WHERE subid=?''', 
              (attended, bunked, percentage, subid))
    conn.commit()
    conn.close()
    
    
def fetchattendance(uid):
    user_id = uid
    conn = sql.connect('attendance.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM attable WHERE id = ?''', [user_id])
    r = c.fetchall()
    conn.commit()
    conn.close()
    return r

def fetchid(username):
    user_name = username
    conn = sql.connect('attendance.db')
    c = conn.cursor()
    c.execute('''SELECT id FROM Users WHERE username = ?''', [user_name])
    r = c.fetchall()
    conn.commit()
    conn.close()
    return r


createusers()
createattable()
# Login page ------------------------------------------------
import tkinter as tk
from tkinter import ttk
import sqlite3
import hashlib
import subprocess
import database as db
import manage
uid = 1
def login():
    username = username_entry.get()
    password = hashlib.sha256(password_entry.get().encode()).hexdigest()

    if not username or not password:
        status_label.config(text="All fields are required", foreground="red")
        return
    
    uid = db.fetchid(username)[0][0]
    print(uid)
    if uid:
        status_label.config(text="Login successful", foreground="green")
        manage.main()
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
# manage ----------------------------------------------
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3 as sql
import database as db
import loginpage
uid = 1
class AttendanceManager:

    def __init__(self, master):
        self.master = master
        self.master.title("Attendance Management System")
        width = 600
        height = 400
        screenwidth = self.master.winfo_screenwidth()
        screenheight = self.master.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.master.geometry(alignstr)
        self.master.resizable(width=False, height=False)
        uid  = 1
        # Database connection
        # self.conn = sql.connect("attend.db")
        # self.cur = self.conn.cursor()
        # self.create_table()

        # Mainframe
        self.mainframe = ttk.Frame(self.master, padding="10")
        self.mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Widgets and Layout
        self.create_widgets()

    # def create_table(self):
    #     self.cur.execute(
    #         'CREATE TABLE IF NOT EXISTS attable(subid INTEGER PRIMARY KEY, subject TEXT, attended INTEGER, bunked INTEGER, percentage INTEGER)')
    #     self.conn.commit()

    def create_widgets(self):
        # Menu
      
        self.menu_label = ttk.Label(
        self.mainframe, text="Attendance Management", font=("Arial", 16),)
        self.menu_label.grid(row=0, column=0, columnspan=2, pady=20)

        self.menu_buttons = [
            ("Add New Record", self.add_new_record),
            ("Manage Attendance", self.manage_attendance),
            ("Delete Record", self.delete_record),
            ("Edit Record", self.edit_record),
            ("Add Subjects", self.add_subjects),
            ("Today's Data", self.today_data),
            ("Exit", self.exit_app)
        ]

        for i, (text, command) in enumerate(self.menu_buttons):
            ttk.Button(self.mainframe, text=text, command=command).grid(
                row=i+1, column=0, pady=5, padx=5, sticky=tk.W+tk.E)

    def add_new_record(self):
        subjects = simpledialog.askstring("Input", "Enter subject names separated by commas (e.g., Maths,Physics):")
        subject = subjects.split(',')
        for sub in subject:
                attended = simpledialog.askinteger(
                    "Input", f"Enter the number of times attended for {subject}:")
                bunked= simpledialog.askinteger(
                    "Input", f"Enter the number of times bunked for {subject}:")
                if attended is not None and bunked is not None:
                    new_attended = attended
                    new_bunked = bunked 
                    percentage = new_attended/(new_attended + new_bunked)*100
                    db.addattendance(sub, new_attended, new_bunked, percentage, uid)
                    messagebox.showinfo('Successful', 'Subjects added :)')
                    
                    
            
        # if subjects:
        #     self.cur.execute('DROP TABLE IF EXISTS attable')
        #     self.create_table()
        #     subjects = subjects.split(",")
        #     for sub in subjects:
        #         self.cur.execute(
        #             'INSERT INTO attable (subject, attended, bunked, percentage) VALUES (?, ?, ?, ?)', (sub.strip(), 0, 0, 0))
        #     self.conn.commit()
        #     messagebox.showinfo("Success", "Subjects added successfully!")

    def manage_attendance(self):
        window = tk.Toplevel(self.master)
        window.title("Manage Attendance")

        # self.cur.execute('SELECT * FROM attable')
        records = db.fetchattendance(1)
        print(records)

        if records:
            for i, (TASKid,subject, attended, bunked,percentage,UID) in records:
                ttk.Label(window, text=f"Task_ID:{TASKid},Subject: {subject}, Attended: {attended}, Bunked: {bunked}, Percentage: {percentage}%, Uid :{UID}").grid(
                    row=i, column=0, pady=5, padx=5)
        else:
            ttk.Label(window, text="No records found.").grid(row=0, column=0)

    def delete_record(self):
        self.cur.execute('DROP TABLE IF EXISTS attable')
        self.conn.commit()
        messagebox.showinfo("Success", "Records deleted!")

    def edit_record(self):
        sub_id = simpledialog.askinteger("Input", "Enter Subject ID:")
        if sub_id:
            self.cur.execute("SELECT * FROM attable WHERE subid=?", (sub_id,))
            record = self.cur.fetchone()

            if record:
                attended = simpledialog.askinteger(
                    "Input", f"Enter number of times attended for {record[1]}:")
                bunked = simpledialog.askinteger(
                    "Input", f"Enter number of times bunked for {record[1]}:")

                if attended is not None and bunked is not None:
                    new_attended = record[2] + attended
                    new_bunked = record[3] + bunked
                    percentage = new_attended/(new_attended + new_bunked)*100
                    self.cur.execute(
                        "UPDATE attable SET attended=?, bunked=?, percentage=? WHERE subid=?", (new_attended, new_bunked, percentage, sub_id))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Record updated successfully!")
                else:
                    messagebox.showerror("Error", "Invalid input!")
            else:
                messagebox.showerror("Error", "Subject ID not found!")

    def add_subjects(self):
        subjects = simpledialog.askstring(
            "Input", "Enter subject names separated by commas (e.g., Math,Science):")
        if subjects:
            subjects = subjects.split(",")
            for sub in subjects:
                self.cur.execute(
                    'INSERT INTO attable (subject, attended, bunked) VALUES (?, ?, ?)', (sub.strip(), 0, 0))
            self.conn.commit()
            messagebox.showinfo("Success", "Subjects added successfully!")

    def today_data(self):
        self.cur.execute('SELECT * FROM attable')
        records = self.cur.fetchall()

        if records:
            for i, (subid, subject, attended, bunked,percentage) in enumerate(records):
                attended_today = simpledialog.askinteger(
                    "Input", f"Enter the number of times attended for {subject}:")
                bunked_today = simpledialog.askinteger(
                    "Input", f"Enter the number of times bunked for {subject}:")
                if attended_today is not None and bunked_today is not None:
                    new_attended = attended + attended_today
                    new_bunked = bunked + bunked_today
                    percentage = new_attended/(new_attended + new_bunked)*100
                    self.cur.execute(
                        "UPDATE attable SET attended=?, bunked=? ,percentage=? WHERE subid=?", (new_attended, new_bunked, percentage, subid))
                    self.conn.commit()
            messagebox.showinfo("Success", "Data updated successfully!")
        else:
            messagebox.showerror("Error", "No records found!")

    def exit_app(self):
        self.conn.close()
        self.master.destroy()
        


def main():
    root = tk.Tk()
    root.configure(bg='#f2cc8f')
    app = AttendanceManager(master=root)
    root.mainloop()


main()
# SIGN UP-------------------------------
import tkinter as tk
from tkinter import ttk
import sqlite3
import hashlib
import subprocess
import database as db

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

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

     # Check if the username is already in use
    cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        status_label.config(text="Username already exists", foreground="red")
    else:
        db.adduser(username, password, email)
def open_manager():
    file_path = 'home.py'
    try:
        subprocess.Popen(['python', file_path])
    except FileNotFoundError:
        print("File not found.")

def open_login_page(event):
    root.destroy()
    file_path = 'login.py'
    try:
        subprocess.Popen(['python', file_path])
    except FileNotFoundError:
        print("File not found.")

def on_enter(event):
    style.map("TButton", background=[("active", "#001427")])

def on_leave(event):
    style.map("TButton", background=[("active", "#001427")])


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
