#INTERFACE TO-DO:
#[X]NAGENTS -> SLIDER
#[X]LENGTH OF TAIL -> SLIDER
#[X]SHOW FPS -> TICKBOX
#[X]UNLIMIT FPS -> TICKBOX
#[X]LIMIT FPS -> SLIDER
#[X]COLOUR SCHEME -> DROP DOWN MENU
#[X]CREATE NEW OR LOAD SAVE -> WINDOW WITH TEXT BOX TO ENTER GAMEID -> BUTTON
#[]DELETE PREVIOUS SAVE -> WINDOW WITH TEXT BOX TO ENTER GAMEID -> BUTTON
#[X]INPUT PARAMETERS -> BUTTON
#[]VIEW DATABASE? -> BUTTON
#[X]CREATE CUSTOM COLOUR SCHEME -> CREATE NEW WINDOW TO INPUT ALL COLOURS

from tkinter import *
import sqlite3, os
class interface():
    def __init__(self,gameid):
        print('creating interface')
        self.root = Tk()

        self.gameid = gameid

        self.nodecolour = []
        self.BGcolour = []
        self.agentcolour = []

        self.colourconfigured = False

        self.nagents = IntVar()
        self.taillength = IntVar()
        self.fpslimit = IntVar()
        self.unlimitfps = IntVar(value=1)
        self.showfps = IntVar()

        self.nagentsLabel = Label(self.root,text='Number of Agents').grid(column=0,row=0,columnspan=3)
        self.nagentswarning = Label(self.root,text='(Higher Values Can Severely Impact Performance)',fg='red').grid(column=0,row=1,columnspan=3)
        self.nagentslider = Scale(self.root,from_=1,to=10000,variable=self.nagents,orient=HORIZONTAL,length=400,sliderlength=15).grid(column=0,row=2,columnspan=3)

        self.taillengthLabel = Label(self.root,text='Length of The Agent Tail').grid(column=0,row=3,columnspan=3)
        self.taillengthWarning = Label(self.root,text='(Higher Values Can Severely Impact Performance)',fg='red').grid(column=0,row=4,columnspan=3)
        self.taillengthSlider = Scale(self.root,from_=1,to=100,variable=self.taillength,orient=HORIZONTAL,length=400,sliderlength=15).grid(column=0,row=5,columnspan=3)

        self.fpslimitLabel = Label(self.root,text='FPS limit').grid(column=0,row=6,columnspan=3)
        self.fpslimitWarning = Label(self.root,text='(The Lower The FPS The Slower The Sim)',fg='red').grid(column=0,row=7,columnspan=3)
        self.fpslimitSlider = Scale(self.root,from_=1,to=500,variable=self.fpslimit,orient=HORIZONTAL,length=400,sliderlength=15,command=self.uncheckfps).grid(column=0,row=8,columnspan=3)
        
        self.unlimitFPSbox = Checkbutton(self.root,text='Unlimit FPS',variable=self.unlimitfps,onvalue=1,offvalue=0).grid(column=0,row=9)
        self.showfpsbox = Checkbutton(self.root,text='Show FPS',variable=self.showfps,onvalue=1,offvalue=0).grid(column=1,row=9)

        self.createnewschemeButton = Button(self.root,text='Configure Colour Scheme',command=self.createcolourscheme).grid(column=2,row=9)

        self.exitButton = Button(self.root,text='Exit',command = self.finish,width=56).grid(column=0,row=10,columnspan=3)
        self.root.attributes('-topmost',True)
        self.root.mainloop()

    def uncheckfps(self,event):
        self.unlimitfps = 1

    def finish(self):
        os.system('cls')
        nagents = self.nagents.get()
        taillen = self.taillength.get()
        print('Parameter Settings:')
        print(f'Number of Agents: {nagents}')
        print(f'Length of Agent Tail: {taillen}')
        if self.unlimitfps.get() == 1:
            print('FPS Unlimited')
        else:
            fpslimit = self.fpslimit.get()
            print(f'FPS limited to: {fpslimit}')
        if self.showfps.get() == 1:
            print('FPS Counter Shown')
        else:
            print('FPS Counter Hidden')

        if self.colourconfigured == False:
            self.nodecolour = []
            self.nodecolour.append(0)
            self.nodecolour.append(255)
            self.nodecolour.append(0)

            self.BGcolour = []
            self.BGcolour.append(0)
            self.BGcolour.append(0)
            self.BGcolour.append(0)

            self.agentcolour = []
            self.agentcolour.append(255)
            self.agentcolour.append(255)
            self.agentcolour.append(255)

        else:
            self.getcolourscheme()

        print(f'Agent Colour: {self.agentcolour}')
        print(f'Node Colour: {self.nodecolour}')
        print(f'Background Colour: {self.BGcolour}')
        print(f'GameID: {self.gameid}')

        con = sqlite3.connect('paramaters.db')
        cur = con.cursor()

        addparametersCommand = '''CREATE TABLE IF NOT EXISTS paramaterValues
                                    (gameID INTEGER PRIMARY KEY,nagents INTEGER, taillen INTEGER, unlimitFPS INTEGER, FPSlimit INTEGER, showFPS INTEGER)'''

        cur.execute(addparametersCommand)
        insertcommand = '''INSERT INTO paramaterValues Values (?, ?, ?, ?, ?, ?)'''
        cur.execute(insertcommand, (self.gameid, nagents, taillen, self.unlimitfps.get(), self.fpslimit.get(), self.showfps.get(),))
        con.commit()

        self.root.destroy()

    def createcolourscheme(self):
        self.colourconfigured=True
        root2=Toplevel(self.root)
        CSGUI = loadColourSchemeGUI(root2,self.gameid)

    def getcolourscheme(self):
        con = sqlite3.connect('colourdb.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM ColourScheme")
        results=cur.fetchall()
        for i in range(0,len(results)):
            #NODE COLOUR
            if results[i][0] == 1:
                self.nodecolour.append(results[i][1])
                self.nodecolour.append(results[i][2])
                self.nodecolour.append(results[i][3])

            #BG COLOUR
            if results[i][0] == 2:
                self.BGcolour.append(results[i][1])
                self.BGcolour.append(results[i][2])
                self.BGcolour.append(results[i][3])

            #AGENT COLOUR
            if results[i][0] == 3:
                self.agentcolour.append(results[i][1])
                self.agentcolour.append(results[i][2])
                self.agentcolour.append(results[i][3])
            
class loadColourSchemeGUI():
    def __init__(self,root,gameid):
        self.root=root
        self.root.title('Configure Colour Scheme')
        self.gameid = gameid

        self.r = IntVar()
        self.g = IntVar()
        self.b = IntVar()

        self.nodecolour = []
        self.BGcolour = []
        self.agentcolour = []

        self.agentoption=IntVar()
        self.BGoption=IntVar()
        self.nodeoption=IntVar()

        self.canvasWidth = 50
        self.canvasHeight = 200

        self.canvas = Canvas(self.root,width=self.canvasWidth,height=self.canvasHeight,bg='black')
        self.canvas.grid(column=1,row=1,rowspan=5)

        self.redLabel = Label(self.root,text='Red Value').grid(column=0,row=0)
        self.redSlider = Scale(self.root,from_=0,to=255,orient=HORIZONTAL,variable=self.r,length=255,command=self.updatecanvascolour).grid(column=0,row=1)

        self.greenLabel = Label(self.root,text='Green Value').grid(column=0,row=2)
        self.greenSlider = Scale(self.root,from_=0,to=255,orient=HORIZONTAL,variable=self.g,length=255,command=self.updatecanvascolour).grid(column=0,row=3)

        self.blueLabel = Label(self.root,text='Blue Value').grid(column=0,row=4)
        self.blueSlider = Scale(self.root,from_=0,to=255,orient=HORIZONTAL,variable=self.b,length=255,command=self.updatecanvascolour).grid(column=0,row=5)

        self.agentcolourBox = Button(self.root,text='Agent Colour',command=self.agentcolourCommand).grid(column=2,row=1)
        self.BGcolourBox = Button(self.root,text='Background Colour',command=self.BGcolourCommand).grid(column=2,row=3)
        self.nodeBox = Button(self.root,text='Node Colour',command=self.nodecolourCommand).grid(column=2,row=5)

        self.exitButton = Button(self.root,text='Exit',command=self.finish).grid(column=0,row=6,columnspan=3)

        root.mainloop()

    def updatecanvascolour(self,event):
        r = self.r.get()
        g = self.g.get()
        b = self.b.get()
        hexval = self.rgb_to_hex(r,g,b)
        self.canvas.configure(bg=hexval)

    def agentcolourCommand(self):
        self.agentcolour.append(self.r.get())
        self.agentcolour.append(self.g.get())
        self.agentcolour.append(self.b.get())
    
    def BGcolourCommand(self):
        self.BGcolour.append(self.r.get())
        self.BGcolour.append(self.g.get())
        self.BGcolour.append(self.b.get())

    def nodecolourCommand(self):        
        self.nodecolour.append(self.r.get())
        self.nodecolour.append(self.g.get())
        self.nodecolour.append(self.b.get())

    def rgb_to_hex(self,r,g,b):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)
    
    def finish(self):
        if self.nodecolour == []:
            self.nodecolour.append(0)
            self.nodecolour.append(255)
            self.nodecolour.append(0)

        if self.BGcolour == []:
            self.BGcolour.append(0)
            self.BGcolour.append(0)
            self.BGcolour.append(0)

        if self.agentcolour == []:
            self.agentcolour.append(255)
            self.agentcolour.append(255)
            self.agentcolour.append(255)

        #create database to store colour values

        con = sqlite3.connect('colourdb.db')
        cur = con.cursor()

        createcolourtableCommand = '''CREATE TABLE IF NOT EXISTS ColourScheme
                                    (gameID INTEGER, element_ID INTEGER, R INTEGER, G INTEGER, B INTEGER)'''

        cur.execute(createcolourtableCommand)
        print(self.gameid)
        insertcommand = '''INSERT INTO ColourScheme Values (?, ?, ?, ?, ?)'''
        cur.execute(insertcommand,(int(self.gameid), 1, self.nodecolour[0], self.nodecolour[1], self.nodecolour[2]))
        cur.execute(insertcommand,(int(self.gameid), 2, self.BGcolour[0], self.BGcolour[1], self.BGcolour[2]))
        cur.execute(insertcommand,(int(self.gameid), 3, self.agentcolour[0], self.agentcolour[1], self.agentcolour[2]))
        con.commit()
        self.root.destroy()
        
interface(1)