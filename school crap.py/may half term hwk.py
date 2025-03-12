from tkinter import *

class functionwindow():
    def __init__(self,root):
        
        self.rowlevel = 5
        self.userstring = StringVar()

        self.root = root
        self.root.title('Functions')
        
        self.wordentry = Entry(self.root,textvariable=self.userstring,width=58).grid(row=0,column=0,columnspan=3)

        self.capitalisebut = Button(self.root,command=self.capitalise,text='capitalise',width=15).grid(row=1,column=0)
        self.casefoldbut = Button(self.root,command=self.casefold,text = 'casefold',width=16).grid(row=1,column=1)
        self.isidentifierbut = Button(self.root,command=self.isidentifier,text='isidentifier',width=15).grid(row=1,column=2)

        self.isidentifierbut = Button(self.root,command=self.isspace,text='isspace',width=15).grid(row=2,column=0)
        self.isidentifierbut = Button(self.root,command=self.endswith,text='endswith',width=16).grid(row=2,column=1)
        self.isidentifierbut = Button(self.root,command=self.islower,text='islower',width=15).grid(row=2,column=2)

        self.isidentifierbut = Button(self.root,command=self.isalnum,text='isalnum',width=15).grid(row=3,column=0)
        self.isidentifierbut = Button(self.root,command=self.isdecimal,text='isdecimal',width=16).grid(row=3,column=1)
        self.isidentifierbut = Button(self.root,command=self.isdigit,text='isdigit',width=15).grid(row=3,column=2)

        self.clearbut = Button(self.root,command=self.clear,text='Clear',width=49).grid(row=4,column=0,columnspan=3)

    def capitalise(self):
        self.capitaliselabel = Label(self.root,text=f'capitalise: {self.userstring.get().capitalize()}').grid(row=self.rowlevel,column=0)
        self.rowlevel+=1

    def casefold(self):
        self.casefoldlabel = Label(self.root,text=f'casefold: {self.userstring.get().lower()}').grid(row=self.rowlevel,column=0)
        self.rowlevel+=1

    def isidentifier(self):
        self.isidentifierlabel = Label(self.root,text=f'isidentifier: {self.userstring.get().isidentifier()}').grid(row=self.rowlevel,column=0)
        self.rowlevel+=1

    def isspace(self):
        self.isspacelabel = Label(self.root,text=f'isspace: {self.userstring.get().isspace()}').grid(row=self.rowlevel,column=0)
        self.rowlevel+=1

    def endswith(self):
        root2 = Toplevel(self.root)
        self.finalcharacter = self.userstring.get()
        self.character = entrywindow(root2,self.finalcharacter)
            

    def islower(self):

        self.islowerlabel = Label(self.root,text=f'islower: {self.userstring.get().islower()}').grid(row=self.rowlevel,column=0)
        self.rowlevel+=1

    def isalnum(self):
        self.isalnum = Label(self.root,text=f'isalnum: {self.userstring.get().isalnum()}').grid(row=self.rowlevel,column=0)
        self.rowlevel+=1

    def isdecimal(self):
        self.isdecimallabel = Label(self.root,text=f'isdecimal: {self.userstring.get().isdecimal()}').grid(row=self.rowlevel,column=0)
        self.rowlevel+=1

    def isdigit(self):
        self.isdigit = Label(self.root,text=f'isdigit: {self.userstring.get().isdigit()}').grid(row=self.rowlevel,column=0)
        self.rowlevel+=1

    def clear(self):
        self.root.withdraw()
        root=Tk()
        startfunctions = functionwindow(root)

class entrywindow():
    def __init__(self,root,finalcharacter):
        self.endswithcharacter = StringVar()
        self.finalcharacter = finalcharacter
        self.root2 = root
        self.root2.title('endswith entry')

        self.entrylabel = Label(self.root2,text="Enter Your 'endswith' Character").grid(column=0,row=0)
        self.entrybox = Entry(self.root2,textvariable=self.endswithcharacter,width=30).grid(column=0,row=1)
        self.enterbut = Button(self.root2,text='Input Character',command = self.getcharacter).grid(column=0,row=2)
        self.backbut = Button(self.root2,text='Back',command=self.withdraw).grid(column=0,row=3)

    def getcharacter(self):
        self.letter = self.endswithcharacter.get()[0]
        if self.finalcharacter == self.letter:
            self.truelabel = Label(self.root2,text='True').grid(column=0,row=4)

        else:
            self.truelabel = Label(self.root2,text='False').grid(column=0,row=4)

    def withdraw(self):
        self.root2.withdraw()
        

def main():
    root = Tk()
    startfunctions = functionwindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()