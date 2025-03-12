from tkinter import *

class Welcome():
    def __init__(self,master):
        self.master = master
        self.master.geometry('400x200+100+200')
        self.master.title('WELCOME')


        self.WelcomeLabel=Label(self.master,text='Welcome to the wages calculator GUI',fg='red').place(x=0,y=2)
        self.OKButton=Button(self.master,text="OK",fg='blue',command=self.wages).place(x=10,y=20)
        self.QuitButton=Button(self.master,text="QUIT",fg='blue',command=self.finish).place(x=40,y=20)
        

    def wages(self):
        root2=Toplevel(self.master)
        muGUI=WageWindow(root2)

    def finish(self):
        self.master.destroy()

class WageWindow():
    def __init__(self,master):

        self.nhours=DoubleVar()
        self.salaryh =DoubleVar()
        self.tLevel =DoubleVar()

        self.master=master

        self.master.geometry('500x200+100+200')
        self.master.title('Wages Calculator')

        self.WelcomeLabel = Label(self.master,text='Welcome to the wages calculator GUI',fg='red').grid(row=0,column=2)
        self.SalaryLabel =Label(self.master,text='Enter your salary per hour').grid(row=3,column=0)

        self.HoursWorkedLabel = Label(self.master,text='Enter the hours worked').grid(row=4,column=0)

        self.taxRateLabel = Label(self.master,text='Enter your tax rate').grid(row=5,column=0)
        

        self.taxBut = Button(self.master,text='Calculate tax',fg='Blue',command=self.calculatetax).grid(row=6,column=0)


        self.mysalary = Entry(self.master,textvariable=self.salaryh).grid(row=3,column=2)
        self.myhours = Entry(self.master,textvariable=self.nhours).grid(row=4,column=2)

        self.CalcButton=Button(self.master,text='Calculate Salary',fg='blue',command=self.calculatesalary).grid(row=6,column=2)
        self.QuitButton=Button(self.master,text='Back',fg='blue',command=self.myquit).grid(row=6,column=4)

        self.taxlevel = Entry(self.master,textvariable=self.tLevel).grid(row=5,column=2)

    def calculatesalary(self):
        hours=self.nhours.get()
        print(hours)
        hsal=self.salaryh.get()
        salary = hsal*hours
        print(salary)
        self.labelresult=Label(self.master,text="your salary is: £ %.2f" % salary).grid(row=7,column =2)

    def calculatetax(self):
        taxrate = self.tLevel.get()
        hours = self.nhours.get()
        hsal=self.salaryh.get()
        salary = hsal*hours
        taxrate=taxrate/100
        taxpaid=salary*taxrate
        print(taxpaid)
        self.Labeltax=Label(self.master,text="your tax is: £ %.2f" % taxpaid).grid(row=9,column=2)





    def myquit(self):
        self.master.destroy()

def main():
    root=Tk()
    myGUIWelcome=Welcome(root)
    root.mainloop()

if __name__ == '__main__':
    main()