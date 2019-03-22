from tkinter import *
from tkinter.ttk import *
from random import random, choice, randint
import pyperclip
from pathlib import Path

class VaultApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        
        icon_folder = Path("data/")
        icon = icon_folder / "icon.ico"
        self.title('Passtorage 0.1b1')
        self.iconbitmap(icon)
        self.minsize(300, 300)
        self.geometry("300x300")
        self.switch_frame(HomePage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class HomePage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text="Main Menu").grid(columnspan=2)
        Button(self, text="Generate New Password", width=25, command=lambda: master.switch_frame(GenerationPage)).grid(
            columnspan=2, pady=5)
        

class GenerationPage(Frame):
    

    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text="Generator").grid(row=0, columnspan=2)
        
        Label(self, text="Password Name:").grid(row=1, column=0)
        global ent
        ent = Entry(self, width=20)
        ent.grid(row=1, column=1)
        
        pl = Label(self, text="Password Length:")
        pl.grid(row=2, column=0)
        sp = Spinbox(self, values=("8", "10", "12", "14", "16"), width=18)
        sp.insert(0, 8)
        sp.grid(row=2, column=1, pady=5)

        
        gb = Button(self, text="Generate", width=20, command=lambda: gen())
        gb.grid(row=4, column=0, pady=5)

        
        gpl = Label(self, text="", width=20)
        gpl.grid(row=3, columnspan=2)

        def gen():
            length = int(sp.get())
            capitals = "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
            letters = "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
            digits = "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"
            
            chars = capitals + letters + digits
            global password
            password = "".join(choice(chars)
                               for x in range(randint(length, length)))
            gpl.config(text=password)

        
        cp = Button(self, text="Copy", width=20, command=lambda: copy())
        cp.grid(row=4, column=1, pady=5)

        def copy():
            pyperclip.copy(password)

       
        sb = Button(self, text="Save", width=20, command=lambda: autosave())
        sb.grid(row=5, column=1, pady=5)

        def autosave():
            data_folder = Path("data/reg/test")            
            title = str(ent.get())
            file_to_open = data_folder / title
            file = open((file_to_open), "a")
            file.write(str(password))
            file.close()

        
        Button(self, text="Return to main menu", width=25, command=lambda: master.switch_frame(HomePage)).grid(
            row=6,
            columnspan=2)





if __name__ == "__main__":
    app = VaultApp()
    app.style = Style()
    app.style.theme_use("vista")
    app.mainloop()
    
