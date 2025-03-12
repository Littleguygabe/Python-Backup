from tkinter import *
root = Tk()

variabletest = int(input('input a number: '))
variableCheck = Label(root, text=variabletest)

variableCheck.pack()

root.mainloop()