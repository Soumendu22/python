import tkinter as tk
from tkinter import ttk

def on_enter(event):
    style.map("TButton", background=[("active", "blue")])

def on_leave(event):
    style.map("TButton", background=[("active", "red")])

root = tk.Tk()

style = ttk.Style()

# Create a custom style for the button
style.configure("Custom.TButton", background="red")

button = ttk.Button(root, text="Hover Over Me", style="Custom.TButton")
button.pack()

button.bind("<Enter>", on_enter)
button.bind("<Leave>", on_leave)

root.mainloop()
