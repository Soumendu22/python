import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3 as sql


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

        # Database connection
        self.conn = sql.connect("attend.db")
        self.cur = self.conn.cursor()
        self.create_table()

        # Mainframe
        self.mainframe = ttk.Frame(self.master, padding="10")
        self.mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Widgets and Layout
        self.create_widgets()

    def create_table(self):
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS attable(subid INTEGER PRIMARY KEY, subject TEXT, attended INTEGER, bunked INTEGER, percentage INTEGER)')
        self.conn.commit()

    def create_widgets(self):
        # Menu
        self.menu_label = ttk.Label(
            self.mainframe, text="Attendance Management System", font=("Arial", 16),)
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
        subjects = simpledialog.askstring(
            "Input", "Enter subject names separated by commas (e.g., Maths,Physics):")
        if subjects:
            self.cur.execute('DROP TABLE IF EXISTS attable')
            self.create_table()
            subjects = subjects.split(",")
            for sub in subjects:
                self.cur.execute(
                    'INSERT INTO attable (subject, attended, bunked, percentage) VALUES (?, ?, ?, ?)', (sub.strip(), 0, 0, 0))
            self.conn.commit()
            messagebox.showinfo("Success", "Subjects added successfully!")

    def manage_attendance(self):
        window = tk.Toplevel(self.master)
        window.title("Manage Attendance")

        self.cur.execute('SELECT * FROM attable')
        records = self.cur.fetchall()

        if records:
            for i, (subid, subject, attended, bunked,percentage) in enumerate(records):
                ttk.Label(window, text=f"Subject: {subject}, Attended: {attended}, Bunked: {bunked}, Percentage: {percentage}%").grid(
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
    app = AttendanceManager(master=root)
    root.mainloop()


if __name__ == "__main__":
    main()