from tkinter import *
root = Tk()
import random
hexAns = []

def createHex():
    Hexvalue = random.randint(0,255)
    print(Hexvalue)
    Hexnumber = hex(Hexvalue)
    hexAns.clear()
    for i in range (0,(len(str(Hexnumber)))):
        hexAns.append(Hexnumber[i])

def giveAns():
    if len(hexAns)>=3:
        hexAns.remove('0')
        hexAns.remove('x')
        print(hexAns)
    
    else:
        print(hexAns)

hexGenerate = Button(root, text = 'Generate Hex Number', command=createHex, padx=110, pady=60, bg = '#e494ff')
hexGiveAns = Button(root, text = 'Give Hexadecimal Answer', command=giveAns, padx=100, pady=60, bg = '#89CFF0')
ansBox = Entry(root)

hexGenerate.pack()
hexGiveAns.pack()
ansBox.pack()

root.mainloop()