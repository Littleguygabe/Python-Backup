from tkinter import *
root = Tk()
import random
ansArray = []

def generateNumber():
    num1 = random.randint(1,99)
    num2 = random.randint(1,99)
    answer = num1*num2

    ansArray.clear()
    ansArray.append(answer)

    print('Your Two Numbers Are...')
    print(num1)
    print(num2)
    
def printNumber():
    print(ansArray)

numGen = Button(root, text = 'generate 2 New Numbers', command=generateNumber, padx=100, pady=60, bg = '#e494ff')
numPrint = Button(root, text = 'Print Answer', command=printNumber, padx=134, pady=60, bg = '#89CFF0')


numGen.pack()
numPrint.pack()

root.mainloop()