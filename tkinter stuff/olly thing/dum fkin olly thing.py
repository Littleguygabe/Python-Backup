from tkinter import *
root = Tk()
import random

def flip_coin():
    result = random.randint(1,2)
    if result == 2:
        print('heads')

    elif result == 1:
        print('tails')

    else:
        print('idfk what just happened cause it shouldnt have happened')


flip = Button(root, text='flip a coin!',padx = 100, pady = 60, command=flip_coin)

flip.pack()
root.mainloop()