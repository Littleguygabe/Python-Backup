from tkinter import *
root = Tk()
coefficients = []

def differentiate(equation):
    neweq = []
    print(equation)
    for mainarrayindex in range(0,len(equation)):
        coefficientarray=[]
        tempcoefficientarray = equation[mainarrayindex][0]
        power = equation[mainarrayindex][1]
        power = int(power)

        for i in range(0,len(tempcoefficientarray)):
            coefficientarray.append(tempcoefficientarray[i])

        coefficient=coefficientarray[0]
        symbol=coefficientarray[1]
        
        if power == 1:
            neweq.append(coefficient)

        else:
            newcoefficient = str(power*int(coefficient))
            newpower = str(power-1)
            neweq.append(newcoefficient+symbol+'^'+newpower)



    print(neweq)

def createEquation():
    equation = []
    for y in range(0,len(coefficients),2):
        temparray = []

        coefficientEntry = coefficients[y]
        temparray.append(coefficientEntry.get())

        powerEntry = coefficients[y+1]
        power = powerEntry.get()
        if power==1:
            print('no change')
        else:
            temparray.append(power)
        equation.append(temparray)

    differentiate(equation)

def addCoefficient():
    x=1

    #base number
    coefficients.append(Entry(root,
                              width=5,
                            ))
    
    coefficients.append(Entry(root,
                              width=3,   
                            ))
     
    for i in range(0,len(coefficients),2):
        coefficients[i].grid(row = 1,column = x)
        x=x+1
        coefficients[i+1].grid(row=0,column=x)
        x=x+1

differntiatiateBut = Button(root,text='Differentiate',padx=50,pady=30,command = createEquation)
addCoefBut = Button(root,text = 'Add Coefficient',padx=42,command = addCoefficient)

differntiatiateBut.grid(rowspan=2,row=1,column=0)
addCoefBut.grid(row=0,column = 0)

root.mainloop()