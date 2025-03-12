from random import random
from pyfirmata import Arduino, SERVO, util
import keyboard, sys

from tkinter import *
root = Tk()

lq = 0
rq = 0
lc = 0
rc = 0
port = 'COM3'
board=Arduino(port)
pin1 = 2 #left quad
pin2 = 3 # right quad
pin3 = 4 #left control
pin4 = 5 #right control

interval = 2

maxlq = 0
maxlc = 120
maxrq = 120
maxrc = 0

minlq = 120-maxlq
minlc = 120-maxlc
minrq = 120-maxrq
minrc = 120-maxrc

board.digital[pin1].mode=SERVO
board.digital[pin2].mode=SERVO
board.digital[pin3].mode=SERVO
board.digital[pin4].mode=SERVO

board.digital[pin1].write(minlq)
board.digital[pin2].write(minrq)
board.digital[pin3].write(minlc)
board.digital[pin4].write(minrc)

def quit():
    sys.exit()

def moveMinHeight():
    board.digital[pin1].write(minlq)
    board.digital[pin2].write(minrq)
    board.digital[pin3].write(minlc)
    board.digital[pin4].write(minrc) 

def moveMaxHeight():
    board.digital[pin1].write(maxlq)
    board.digital[pin2].write(maxrq)
    board.digital[pin3].write(minlc)
    board.digital[pin4].write(minrc)   

ButtonQuit = Button(root,
                    text='Quit',
                    command=quit
                    )

Buttonminheight = Button(root,
                    text = 'min height',
                    command=moveMinHeight)

buttonMaxheight = Button(root,
                        text='max height',
                        command=moveMaxHeight)

ButtonQuit.pack()
Buttonminheight.pack()
buttonMaxheight.pack()
print('ready')

root.mainloop()