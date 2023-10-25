import tkinter as tk
import tkinter.font as tkFont
import subprocess

class App:
    def __init__(self, root):
        #setting title
        
        root.title("Attendance Manager-Faculty")
        #setting window size
        width=600
        height=400
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        

        GMessage_108=tk.Message(root)
        ft = tkFont.Font(family='Times',size=28)
        GMessage_108["font"] = ft
        GMessage_108["bg"] = "#ffd6ff"
        GMessage_108["fg"] = "#264653"
        GMessage_108["justify"] = "center"
        GMessage_108["text"] = "WELCOME TO ATTENDANCE MANAGER"
        GMessage_108["relief"] = "flat"
        GMessage_108.place(x=00,y=50,width=598,height=170)

        GButton_971=tk.Button(root)
        GButton_971["bg"] = "#c8b6ff"
        ft = tkFont.Font(family='Times',size=13)
        GButton_971["font"] = ft
        GButton_971["fg"] = "#000000"
        GButton_971["justify"] = "center"
        GButton_971["text"] = "Signup"
        GButton_971.place(x=200,y=250,width=78,height=30)
        GButton_971["command"] = self.GButton_971_command
     

        GButton_803=tk.Button(root)
        GButton_803["bg"] = "#c8b6ff"
        ft = tkFont.Font(family='Times',size=13)
        GButton_803["font"] = ft
        GButton_803["fg"] = "#000000"
        GButton_803["justify"] = "center"
        GButton_803["text"] = "Login"
        GButton_803.place(x=320,y=250,width=78,height=30)
        GButton_803["command"] = self.GButton_803_command

        
    def GButton_971_command(self):
        file_path = 'signupfaculty.py'
        try:
                subprocess.Popen(['python', file_path])
        except FileNotFoundError:
                print("File not found.")
        root.destroy()


    def GButton_803_command(self):
        file_path = 'loginfaculty.py'
        try:
                subprocess.Popen(['python', file_path])
        except FileNotFoundError:
                print("File not found.")
        root.destroy()

    

    
if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='#ffd6ff')
    app = App(root)
    root.mainloop()
