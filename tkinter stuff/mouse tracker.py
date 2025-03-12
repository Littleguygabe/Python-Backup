import tkinter as tk
from tkinter import *
import random
import time
root = tk.Tk()
x=0

root.geometry('1920x820')


def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))


#place new button

def new_place():
    randX = random.randint(1,1870)
    randY = random.randint(1,1030)
    button.place(x=randX, 
                y = randY,
                in_=root)
    x=x+1

#button definition

button = tk.Button(root,
                padx=50,
                pady=50,
                bg = 'red',
                state='active',
                command = new_place,
                )

#start random position
randX = random.randint(1,1870)
randY = random.randint(1,1030)
button.place(x=randX, 
            y = randY,
            in_=root)

root.attributes('-fullscreen', True)

root.bind('<Motion>', motion)
root.mainloop()

#535, 465