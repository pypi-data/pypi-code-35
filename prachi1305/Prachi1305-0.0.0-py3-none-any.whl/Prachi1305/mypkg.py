from tkinter import *

root = Tk()
root.title("My First GUI")
root.geometry("400x300+300+250")

def f1():
	root.configure(background="red")
btnRed = Button(root, text="Red", width=10, command=f1)
def f2():
	root.configure(background="light green")
btnGreen = Button(root, text="Green", width=10, command=f2)
def f3():
	root.configure(background="#0000ff")
btnBlue = Button(root, text="Blue", width=10, command=f3)

btnRed.pack(pady=20)
btnGreen.pack(pady=20)
btnBlue.pack(pady=20)


root.mainloop()




