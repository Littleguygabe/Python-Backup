from tkinter import *
from idlelib.tooltip import Hovertip
import ctypes, dbfunctions, main, re
from functools import *
from tkinter import messagebox
from tkinter import ttk

class stack():
    def __init__(self) -> None:
        self.__stack = []
    
    def push(self,x):
        self.__stack.append(x)
    
    def pop(self):
        return(self.__stack.pop())
        
    def peak(self):
        return self.__stack[-1]
    
    def is_empty(self):
        if len(self.__stack) == 0:
            return True
        else:
            return False

class access():
    def __init__(self) -> None:
        self.menuStack = stack()
        loginPage(self.menuStack)

class agentConfigDimensions():
    windowHeight = 330
    user32 = ctypes.windll.user32
    screen_width,screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    windowWidth=int(screen_width*0.2)
    windowX = 150
    windowY = 150

class loginPage(agentConfigDimensions):
    def __init__(self,menuStack):
        self.count = 0
        self.windowX = agentConfigDimensions.windowX
        self.windowY = agentConfigDimensions.windowY
    
        self.menuStack = menuStack
        
        self.windowWidth = 200
        self.windowHeight = 190        
        self.root = Tk()
        self.root.geometry('{}x{}+{}+{}'.format(self.windowWidth,
                                                self.windowHeight,
                                                self.windowX,
                                                self.windowY))
        self.root.title('Login Page')
        self.username = StringVar()
        self.password = StringVar()
        
        self.createInterface()
        
        self.root.mainloop()

    def createInterface(self):
        #Username       
        self.usernameLabel = Label(self.root,
                                   text='Username')
        self.usernameLabel.grid(column=0,row=0)
        
        self.usernameEntry = Entry(self.root,
                                   textvariable=self.username,
                                   width = self.windowWidth-168,
                                   border=3)
        self.usernameEntry.grid(column=0,row=1)
        
        #password
        self.passwordLabel = Label(self.root,
                                   text='Password')
        self.passwordLabel.grid(column=0,row=2)
        
        self.passwordEntry = Entry(self.root,
                                   textvariable=self.password,
                                   width=self.windowWidth-168,
                                   border=3,
                                   show='●')
        self.passwordEntry.grid(column=0,row=3)
        
        #LOGIN
        #permanent Login
        self.loginBut = Button(self.root,
                               text = 'Login',
                               command=self.login,
                               width=15)
        
        self.loginBut.grid(column=0,row=4)

        
        #guest login
        self.guestLoginBut = Button(self.root,
                                    text='Create New as Guest',
                                    command = self.guestLogin)
        
        self.guestLoginBut.grid(column=0,row=5)
        guestToolTip = Hovertip(self.guestLoginBut,
                                text='Allows Someone Without a Login to Create a Simulation \nHowever the Simulation will not save',
                                hover_delay=0)
        
        self.showPasswordBut = Button(self.root,
                                      text='Show Password',
                                      command = self.showPassword,
                                      padx=12)
        self.showPasswordBut.grid(column=0,row=6)

    def showPassword(self):
        if self.count%2 == 0:
            self.passwordEntry.config(show='')
            self.showPasswordBut.config(text='Hide Password')
            
        else:
            self.passwordEntry.config(show='●')
            self.showPasswordBut.config(text='Show Password')
            
        self.count+=1
        
    def login(self):
        loginAccepted = dbfunctions.login(self.username.get(),self.password.get())
        if loginAccepted == 'admin':
            self.root.destroy()
            #agentConfig(self.username.get() +' - Admin',True,self.username.get(),False,None)
            postLoginoptions(self.username.get() + ' - Admin',True,self.username.get(),self.password.get(),self.menuStack,False)
        
        elif loginAccepted == True:
            self.root.destroy()
            #agentConfig(self.username.get(),False,self.username.get(),False,None)
            postLoginoptions(self.username.get(),False,self.username.get(),self.password.get(),self.menuStack,False)
            
        else:
            loginDenLabel = Label(self.root,
                                  text='Username or Password Incorrect',
                                  fg='red')
            loginDenLabel.grid(column=0,row=7)
      
    def guestLogin(self):
        self.root.destroy()
        agentConfig('Guest',False,'Guest',False,None,self.menuStack)

class postLoginoptions(agentConfigDimensions):
    def __init__(self,userLabel,admin,username,password,menuStack,comeFromBack):
        
        self.password = password
        self.userLabel = userLabel
        self.username = username
        #true or false
        self.admin = admin
        self.windowX = agentConfigDimensions.windowX
        self.windowY = agentConfigDimensions.windowY
        
        self.menuStack = menuStack
        if not comeFromBack:
            tempArr = []
            tempArr.append('postLoginOptions')
            tempArr.append(userLabel)
            tempArr.append(admin)
            tempArr.append(username)
            tempArr.append(password)
            self.menuStack.push(tempArr)
        
        self.windowWidth = 200
        self.windowHeight = 190        
        self.root = Tk()
        self.root.geometry('{}x{}+{}+{}'.format(self.windowWidth,
                                                self.windowHeight,
                                                self.windowX,
                                                self.windowY))
        
        self.root.title(self.userLabel)
        
        self.createinterface()
        
    def createinterface(self):
        self.titleLabel = Label(self.root,
                                text='Options')
        self.titleLabel.pack()
        
        self.newSimBut = Button(self.root,
                                text='Create new Simulation',
                                command = self.createNewSim)
        self.newSimBut.pack()
        
        self.loadSimBut = Button(self.root,
                                 text='Load old Simulation',
                                 command = self.loadSim,
                                 padx=6)
        self.loadSimBut.pack()
        
        self.deleteSaveBut = Button(self.root,
                                    text = 'Delete Save',
                                    command = self.deleteSaves,
                                    padx=25)
        self.deleteSaveBut.pack()
        
        if self.admin == True:            
            self.admincontrolBut = Button(self.root,
                                          text='Admin Controls',
                                          command=self.adminControls,
                                          padx=14)
            self.admincontrolBut.pack()
            
        self.backBut = Button(self.root,
                              text='Back',
                              command = self.back)
        
        self.backBut.pack()
   
    def createNewSim(self):
        self.root.destroy()
        agentConfig(self.userLabel,True,self.username,False,None,self.menuStack)
        
    def loadSim(self):
        hasSaves = dbfunctions.checksaves(self.username)
        if hasSaves:
            self.root.destroy()
            loadSimWindow(self.username,self.admin,self.menuStack)

        else:
            noSavesLabel = Label(self.root,
                                 text='No Sims Saved with that Name',
                                 fg='red')
            noSavesLabel.grid(column=0,row=7)
    
    def adminControls(self):
        self.root.destroy()
        adminControlWindow(self.menuStack)
    
    def back(self):
        self.root.destroy()
        utilities.backFunc(self.menuStack)    
        
    def deleteSaves(self):
        self.root.destroy()
        deleteSaveData(self.username,False,self.menuStack)
    
class deleteSaveData():
    def __init__(self,username,recursive,menuStack):
        self.menuStack = menuStack
        self.username = username
        if recursive == False:
            temparr = []
            temparr.append('deletesavedata')
            temparr.append(username)
            temparr.append(recursive)
            self.menuStack.push(temparr)
        
        self.root = Tk()
        self.createInterface()

    def createInterface(self):
        savesList = dbfunctions.retrieveUserSaves(self.username)
        labelsList = []

        tempArr = []
        tempArr.append('Game ID')
        tempArr.append('Settings Key')
        tempArr.append('Tail Length')
        tempArr.append('Movement Interval')
        tempArr.append('View Distance')
        tempArr.append('Spawn Radius')
        tempArr.append('Dispertion Type')

        headingsLabelList = []
        for string in tempArr:
            headingsLabelList.append(Label(self.root,
                                           text=string,
                                           padx=5))
            
        labelsList.append(headingsLabelList)
        for innerList in savesList:
            innerLL = []
            for string in innerList:
                innerLL.append(Label(self.root,
                              text=str(string),
                              padx=20,
                              pady=10))
            labelsList.append(innerLL)

        for row in range(len(labelsList)):
            for col in range(len(labelsList[row])):
                labelsList[row][col].grid(column=col,row=row)

        buttonsList = []
        for i in range(len(savesList)):
            button = Button(self.root,
                            text='Delete',
                            padx=10)
            button.config(command=partial(self.deleteSave,savesList[i][1]))
            button.grid(column=8,row=i+1)

        backBut = Button(self.root,
                         text='Back',
                         command=self.back)
        
        backBut.grid(column=0,row=len(labelsList)+1)

    def deleteSave(self,settingsKey):
        dbfunctions.deleteSettings(settingsKey)
        self.root.destroy()
        self.__init__(self.menuStack,self.username,True)

    def back(self):
        utilities.backFunc(self.menuStack)
        self.root.destroy()

class adminControlWindow(agentConfigDimensions):
    def __init__(self,menuStack,fromMenuStack = False):
        self.root = Tk()
        self.createInterface()
        self.fromMenuStack = fromMenuStack
    
        if not fromMenuStack:
            self.menuStack = menuStack
            tempArr = []
            tempArr.append('adminControlWindow')
            self.menuStack.push(tempArr)

        
    def createInterface(self):
        self.adminLabel = Label(self.root,
                                    text='Admin Controls',
                                    fg='red')
        self.adminLabel.grid(column=1,row=11,columnspan=2)
        
        #create a new login
        self.createNewLoginLabel = Label(self.root,
                                        text='Create User Login')
        self.createNewLoginLabel.grid(column=0,row=12,columnspan=2)
        self.createNewLoginButton = Button(self.root,
                                            text='Create Login',
                                            command = self.createNewLogin)
        self.createNewLoginButton.grid(column=0,row=13,columnspan=2)
        
        #delete a login 
        self.deleteLoginLabel = Label(self.root,
                                        text='Delete User Login')
        self.deleteLoginLabel.grid(column=2,row=12,columnspan=2)
        self.deleteLoginBut = Button(self.root,
                                        text='Delete Login',
                                        command = self.deleteLogin)
        self.deleteLoginBut.grid(column=2,row=13,columnspan=2)
        
        #View Databases
        self.viewDatabaseLabel = Label(self.root,
                                        text='Display Databases')
        self.viewDatabaseLabel.grid(column=0,row=14,columnspan=2)
        self.viewDataBaseBut = Button(self.root,
                                        text='View db',
                                        command = self.selectTable)
        self.viewDataBaseBut.grid(column=0,row=15,columnspan=2)
        
        self.closeWindowBut = Button(self.root,
                                     text='Back',
                                     command = self.back,
                                     padx=20)
    
        self.closeWindowBut.grid(column=2,row=15,columnspan=2)
    
    def back(self):
        if self.fromMenuStack:
            utilities.backFunc(self.menuStack)

        self.root.destroy()
    
    def selectTable(self):
        tables = dbfunctions.getAllTables()
        root2=Toplevel(self.root)
        tablewin = tableWindow(root2,tables,self.menuStack)
        
    def deleteLogin(self):
        root2 = Toplevel(self.root)
        deleteLoginpage = deleteLoginWindow(root2)

        
    def createNewLogin(self):
        root2 = Toplevel(self.root)
        self.createLogin = createLoginWindow(root2)
        
class loadSimWindow(agentConfigDimensions):
    def __init__(self,username,admin,menuStack):
        self.menuStack = menuStack
        tempArr = []
        tempArr.append('loadSimWindow')
        tempArr.append(username)
        tempArr.append(admin)
        self.menuStack.push(tempArr)
        #true or false
        self.admin = admin
        
        self.windowX = agentConfigDimensions.windowX
        self.windowY = agentConfigDimensions.windowY
        
        self.windowWidth = 465
        self.windowHeight = 190        
        self.root = Tk()
        self.root.geometry('{}x{}+{}+{}'.format(self.windowWidth,
                                                self.windowHeight,
                                                self.windowX,
                                                self.windowY))
        
        self.gameID = IntVar()
        self.gameID.set('')
        self.username = username
        
        self.createInterface()
        
    def createInterface(self):
        self.gIDlabel = Label(self.root,
                              text='Enter a sim ID to Load')
        self.gIDlabel.grid(column=0,row=0,columnspan=7)
        

        self.gIDEntry = Entry(self.root,
                              textvariable=self.gameID)
        self.gIDEntry.grid(column=0,row=1,columnspan=7)
        
        self.loadSettingsBut = Button(self.root,
                                      text='Load Simulation',
                                      command = self.load)   
        self.loadSettingsBut.grid(column=0,row=2,columnspan=7)
        
        self.backButton = Button(self.root,
                                 text='Back',
                                 command = self.back)
        self.backButton.grid(column=0,row=3,columnspan=7)

        usersaves = dbfunctions.retrieveUserSaves(self.username)
        columnNames = dbfunctions.retrieveColumnNames('settings')
        
        for i in range(len(columnNames)):
            if columnNames[i]!=None:
                tempLabel = Label(self.root,
                                  text=columnNames[i],
                                  fg='red')
                tempLabel.grid(column=i,row=4)

        for y in range((len(usersaves))):
            for x in range(len(usersaves[y])):
                tempLabel = Label(self.root,
                                  text=usersaves[y][x],
                                  padx = 0)
                tempLabel.grid(column=x,row=y+5)

    def load(self):
        settings = dbfunctions.getSettings(self.username,self.gIDEntry.get())
        if len(settings) == 0:
            noSaveLabel = Label(self.root,
                                text = 'Invalid Simulation ID',
                                fg = 'red')
            
            noSaveLabel.pack()
            
        else:
            if self.admin == True:
                self.root.destroy()               
                agentConfig(self.username + ' - Admin',True,self.username,True,settings,self.menuStack)
                
            else:
                self.root.destroy()
                agentConfig(self.username,False,self.username,True,settings,self.menuStack)

    def back(self):
        self.root.destroy()
        utilities.backFunc(self.menuStack)

class agentConfig(agentConfigDimensions):
    def __init__(self,usernameLabel,admin,username,fromPrev,settings,menuStack):
        self.menuStack = menuStack
        tempArr = []
        tempArr.append('agentConfig')
        tempArr.append(usernameLabel)
        tempArr.append(admin)
        tempArr.append(username)
        tempArr.append(fromPrev)
        tempArr.append(settings)
        self.menuStack.push(tempArr)
        
        self.fromPrev=fromPrev
        self.root = Tk()
        self.admin = admin
        self.username = username
        self.windowHeight = agentConfig.windowHeight
        self.settings = settings
            
        self.root.geometry('{}x{}+{}+{}'.format(agentConfig.windowWidth,
                                                self.windowHeight,
                                                agentConfig.windowX,
                                                agentConfig.windowY))
        
        self.root.title(usernameLabel)
        
        self.visualisationCreated = False
        
        self.sliderWidth = self.windowWidth-5
        
        self.dispertionMethodArr = ['Standard',
                                    'Spiral',
                                    'X',]
        
        self.curiosityVal = IntVar()
        self.tailLen = IntVar()
        self.movementInterval = IntVar()
        self.viewDistance = IntVar()
        agentConfig.spawnRadius = IntVar()
        self.dispertionMethod = StringVar() 
        self.dispertionMethod.set('Standard')        
        
        if self.fromPrev:
            self.curiosityVal.set(settings[0][1])
            self.tailLen.set(settings[0][2])
            self.movementInterval.set(settings[0][3])
            self.viewDistance.set(settings[0][4])
            self.spawnRadius.set(settings[0][5])
            self.dispertionMethod.set(settings[0][6])
        
        self.createInterface()
        
    def createInterface(self):
        #Curiosity value
        self.curiosityLabel = Label(self.root,text='Agent Curiosity Value')
        self.curiosityLabel.grid(column=1,row=0,columnspan=2)
        
        self.curiosityValSlider = Scale(self.root,
                                        from_=0,to=40,
                                        variable=self.curiosityVal,
                                        orient=HORIZONTAL,
                                        length=self.sliderWidth,sliderlength=15)
        self.curiosityValSlider.grid(column=0,row=1,columnspan=4)
        curiositytip = Hovertip(self.curiosityValSlider,
                                'This Controls how Much an Agent can Vary From the Incentivised Path \n\n Lower Values Result in Straighter, more Controlled Lines \nWhereas Higher Values Result in more Chaotic, Sporadic Lines',
                                hover_delay=0)
        
        #Tail Length Value
        self.tailLenLabel = Label(self.root,text='Tail Length Value')
        self.tailLenLabel.grid(column=1,row=2,columnspan=2)
        
        self.tailLenSlider = Scale(self.root,
                                   from_=1,to=40,
                                   variable=self.tailLen,
                                   orient=HORIZONTAL,
                                   length=self.sliderWidth,sliderlength=15)
        self.tailLenSlider.grid(column=0,row=3,columnspan=4)
        tailLenTip = Hovertip(self.tailLenSlider,
                              'This Controls the Length of the Tail Left Behind the Agent as it Moves \n\nHigher Values can Result in a Decrease in Performance',
                              hover_delay=0)

        #movement interval Value
        self.movementIntervalLabel = Label(self.root,text='Movement Interval Value')
        self.movementIntervalLabel.grid(column=1,row=4,columnspan=2)
        
        self.movementIntervalSlider = Scale(self.root,
                                            from_=1,to=20,
                                            variable=self.movementInterval,
                                            orient=HORIZONTAL,
                                            length=self.sliderWidth,sliderlength=15)
        self.movementIntervalSlider.grid(column=0,row=5,columnspan=4)
        movementIntervalTip = Hovertip(self.movementIntervalSlider,
                                       'This Controls how far an Agent Shifts every Movement \n\nSmaller Values give Smoother Movement but take Longer to reach Nodes \nBigger Values move Quicker but will give a more jumpy Stuttered Motion',
                                       hover_delay=0)
        
        #view distance
        self.viewDistanceLabel = Label(self.root,text='View Distance Value')
        self.viewDistanceLabel.grid(column=1,row=6,columnspan=2)
        
        self.viewDistanceSlider = Scale(self.root,
                                        from_= 0,to = 1000,
                                        variable=self.viewDistance,
                                        orient=HORIZONTAL,
                                        length=self.sliderWidth,sliderlength=15)
        self.viewDistanceSlider.grid(column=0,row=7,columnspan=4)
        
        viewDistanceTip = Hovertip(self.viewDistanceSlider,
                                   'This Controls the Maximum Distance away a node can be Before \n the Agent Stops Moving Towards it ',
                                   hover_delay=0)
        
        #spawn radius
        self.radiusLabel = Label(self.root,text='Spawn Radius Value')       
        self.radiusLabel.grid(column=0,row=8,columnspan=2) 
        self.VisualiseButton = Button(self.root,text = 'Configure Spawn Radius',
                                      command = self.VisualiseSpawnRadius)
        self.VisualiseButton.grid(column=0,row=9,columnspan=2)
        
        spawnRadiusTip = Hovertip(self.VisualiseButton,
                                  'This Controls the size of the Radius of the Spawn Circle \n\nThe Button will open the Config Window for the Spawn Radius',
                                  hover_delay=0)
        
        #dispertion method
        self.dispertionLabel = Label(self.root,text='Dispersion Method')
        self.dispertionLabel.grid(column=2,row=8,columnspan=2)
        
        self.dispertionDropDown = OptionMenu(self.root,
                                             self.dispertionMethod,
                                             *self.dispertionMethodArr)
        self.dispertionDropDown.grid(column=2,row=9,columnspan=2)
        
        dropdownTip = Hovertip(self.dispertionDropDown,
                               'Standard - The Agents move out from the Starting Positions in a wave-like Formation \nSpiral - The Agents move out from the Starting Positions in a Clockwise Spiral Formation \nX - The Agents move out from the Starting Positions in an X Shaped Formation ',
                               hover_delay=0)
        
        self.finishBut = Button(self.root,
                                text='Run Simulation',
                                command = self.inputParameters,
                                width=int((self.windowWidth)/14.28))
        self.finishBut.grid(column=0,row=10,columnspan=2)  
        
        self.backBut = Button(self.root,
                              text = 'Back',
                              command = self.back,
                              width=int((self.windowWidth)/14.28))
        self.backBut.grid(column=2,row=10,columnspan=2)
        
        self.root.mainloop()
             
    def back(self):
        self.root.destroy()
        utilities.backFunc(self.menuStack)
             
    def VisualiseSpawnRadius(self):
        #self.VisualiseButton.config(state='disabled')
        root2=Toplevel(self.root)
        self.spawnRadiusWindow = loadVisualisation(root2,self.spawnRadius.get()) ######
        
    def inputParameters(self):
        if not self.fromPrev:
            if self.username != 'Guest':
                gameID = dbfunctions.generateGameId(self.username)
                settingsKey = dbfunctions.createSettingsId()
                dbfunctions.createLinkRegister(self.username,gameID,settingsKey)
                dbfunctions.enterParameters(settingsKey,
                                        self.curiosityVal.get(),
                                        self.tailLen.get(),
                                        self.movementInterval.get(),
                                        self.viewDistance.get(),
                                        self.spawnRadius.get(),
                                        self.dispertionMethod.get().lower()
                                        )
                
                self.root.destroy()
                main.startprogram(settingsKey,False)
                
            else:
                self.root.destroy()
                gameID = dbfunctions.generateGameId(self.username)
                settingsKey = dbfunctions.createSettingsId()
                dbfunctions.createLinkRegister('guest',gameID,settingsKey)
                dbfunctions.enterParameters(settingsKey,
                                        self.curiosityVal.get(),
                                        self.tailLen.get(),
                                        self.movementInterval.get(),
                                        self.viewDistance.get(),
                                        self.spawnRadius.get(),
                                        self.dispertionMethod.get().lower()
                                        )
                main.startprogram(settingsKey,True)
                
        else:
            dbfunctions.updateSettings(self.settings[0][0],
                                    self.curiosityVal.get(),
                                    self.tailLen.get(),
                                    self.movementInterval.get(),
                                    self.viewDistance.get(),
                                    self.spawnRadius.get(),
                                    self.dispertionMethod.get().lower())
        #Database manipulation

            self.root.destroy()
            main.startprogram(self.settings[0][0],fromPrev=self.fromPrev)
                
        self.root.destroy()
        main.startprogram(settingsKey)
               
class loadVisualisation(agentConfigDimensions): #No need to back track from stack
    def __init__(self,root,InitialspawnRadius):
        self.windowX = agentConfigDimensions.windowX+agentConfigDimensions.windowWidth
        self.windowY = agentConfigDimensions.windowY
        self.root = root
        self.root.attributes('-topmost',True)
        
        self.windowWidth = int((agentConfigDimensions.windowWidth)*1.5+50)
        self.windowHeight = int((agentConfigDimensions.windowWidth)*1.5+145)
        
        self.spawnRadius = IntVar()
        self.spawnRadius.set(InitialspawnRadius)
        
        self.root.geometry('{}x{}+{}+{}'.format(self.windowWidth,
                                                self.windowHeight,
                                                self.windowX,
                                                self.windowY))
        
        self.createInterface()
          
    def createInterface(self):
        self.canvasHeight = self.windowWidth-5
        self.canvasWidth = self.windowWidth-5
        self.canvas = Canvas(self.root,
                             height = self.canvasHeight,
                             width = self.canvasWidth,
                             bg='black')
        
        self.canvas.grid(column=0,row=0,columnspan=3)
        
        #spawn Radius Adjustment
        self.radiusLabel = Label(self.root,text='Spawn Radius Adjustment')
        self.radiusLabel.grid(column=1,row=1)
        
        self.radiusSlider = Scale(self.root,
                                  from_=20,to=300,
                                  orient=HORIZONTAL,
                                  variable=self.spawnRadius,
                                  length=self.canvasWidth,sliderlength=15,
                                  command=self.updateCircle)

        self.radiusSlider.grid(column=0,row=2,columnspan=3)
        
        self.updateCircle(self.spawnRadius.get())
        self.finishBut = Button(self.root,
                                text='Finish Adjusting',
                                command=self.quit,
                                width=int(self.canvasWidth/7.14))
        
        self.finishBut.grid(column=0,row=3,columnspan=3)      
        
    def updateCircle(self,event):
        self.canvas.delete('all')
        x0 = (self.canvasWidth/2)-self.spawnRadius.get()
        y0 = (self.canvasHeight/2)-self.spawnRadius.get()
        x1 = (self.canvasWidth/2)+self.spawnRadius.get()
        y1 = (self.canvasHeight/2)+self.spawnRadius.get()
        self.canvas.create_oval(x0, y0, x1, y1,outline='white')
        
    def quit(self):
        agentConfig.spawnRadius.set(self.spawnRadius.get())
        self.root.destroy()
               
class createLoginWindow(agentConfigDimensions):
    def __init__(self,root):
        self.adminOption = IntVar()
        self.newUsername = StringVar()
        self.newPassword = StringVar()
        self.newPasswordConfirm = StringVar()
        
        self.windowX = agentConfigDimensions.windowX
        self.windowY = agentConfig.windowHeight+agentConfigDimensions.windowY+230
        self.windowWidth = agentConfig.windowWidth
        self.windowHeight = int((agentConfigDimensions.windowWidth)*1.5-35)-(agentConfigDimensions.windowY+230)
        self.root = root
        
        self.root.geometry('{}x{}+{}+{}'.format(self.windowWidth,
                                                self.windowHeight,
                                                self.windowX,
                                                self.windowY))
        
        self.createInterface()
        
    def createInterface(self):
        #username
        self.usernameLabel = Label(self.root,
                                   text='New Username')
        self.usernameLabel.grid(column=0,row=0,columnspan=2)
        
        self.usernameEntry = Entry(self.root,
                                   textvariable=self.newUsername,
                                   border=3,
                                   width=int(self.windowWidth/14.2))
        self.usernameEntry.grid(column=0,row=1,columnspan=2)
        
        #password
        self.passwordLabel = Label(self.root,
                                   text='New Password')
        self.passwordLabel.grid(column=0,row=2)
        
        self.passwordEntry = Entry(self.root,
                                   textvariable=self.newPassword,
                                   border=3,
                                   width=int((self.windowWidth/14.2)))
        self.passwordEntry.grid(column=0,row=3)
        
        #Confirm Password
        self.passwordConfirmLabel = Label(self.root,
                                          text='Confirm Password')
        self.passwordConfirmLabel.grid(column=1,row=2)
        
        self.passwordConfirmEntry = Entry(self.root,
                                          textvariable=self.newPasswordConfirm,
                                          border=3,
                                          width=int((self.windowWidth)/14.2))
        self.passwordConfirmEntry.grid(column=1,row=3)
        
        #Create User       
        self.createUserBut = Button(self.root,
                                    text='Create User',
                                    command=self.createUser,
                                    width=int(self.windowWidth/7.1))
        self.createUserBut.grid(column=0,row=5,columnspan=2)
        
        #admin Check box
        self.admincheckBox = Checkbutton(self.root,
                                         text='Admin',
                                         variable = self.adminOption,
                                         onvalue=1, offvalue=0)
        
        self.admincheckBox.grid(column=0,row=4,columnspan=2)
        
        self.backBut = Button(self.root,
                              text='Back',
                              command=self.back,
                              width = int(self.windowWidth/7.1))
        self.backBut.grid(column=0,row=6,columnspan=2)
        
    def createUser(self):
        empty = True
        for character in self.newPassword.get():
            if character != '' or character != ' ':
                empty = False
        if empty == False:
            if self.newPassword.get() != self.newPasswordConfirm.get():
                utilities.errorBox('Passwords do not Match')
            
            else:
                
                pattern = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$')
                result = pattern.match(self.newPassword.get())
                if result!=None:
                    
                    #check that username doesn't already exist
                    userExists = dbfunctions.checkUsernameAlreadyExists(self.newUsername.get())
                    if userExists:
                        utilities.errorBox('Username Already Exists')
                    else:
                        dbfunctions.createNewUser(self.newUsername.get(),self.newPassword.get(),self.adminOption.get())
                        self.root.destroy()
                        messagebox.showinfo('showInfo','User has been created')
                    
                else:
                    if len(self.newPassword.get())<8:
                        utilities.errorBox('Password too Short\nMust be at Least 8 Characters')
                        
                    else:
                        pattern = re.compile(r'(?=.*[A-Z])')
                        result = pattern.match(self.newPassword.get())
                        if result == None:
                            utilities.errorBox('Need an Uppercase Letter')
                            
                        else:
                            utilities.errorBox('Need a Number')
                            
        else:
            utilities.errorBox('Password Cannot be Blank')
                        
                
    def back(self):
        self.root.destroy()
             
class deleteLoginWindow(agentConfigDimensions):
    def __init__(self,root):        
        self.root = root
        self.windowX = agentConfigDimensions.windowX
        self.windowY = agentConfig.windowHeight+agentConfigDimensions.windowY+230
        self.windowWidth = agentConfig.windowWidth
        self.windowHeight = int((agentConfigDimensions.windowWidth)*1.5-35)-(agentConfigDimensions.windowY+230)
        
        self.root.geometry('{}x{}+{}+{}'.format(self.windowWidth,
                                                self.windowHeight,
                                                self.windowX,
                                                self.windowY))
        
        self.username = StringVar()
        self.password = StringVar()
        self.deleteUsername = StringVar()
        
        self.createInterface()
        
    def createInterface(self):
        #username
        self.adminusernameLabel = Label(self.root,
                                   text='Your Login Username')
        self.adminusernameLabel.grid(column=0,row=0)
        self.adminusernameEntry = Entry(self.root,
                                   textvariable=self.username,
                                   width=int((self.windowWidth/14.2)),
                                   border=3)
        self.adminusernameEntry.grid(column=0,row=1)
        
        #password
        self.passwordLabel = Label(self.root,
                                   text='Your Login Password')
        self.passwordLabel.grid(column=1,row=0)
        self.passwordEntry = Entry(self.root,
                                   textvariable=self.password,
                                   width=int((self.windowWidth/14.2)),
                                   border=3)
        self.passwordEntry.grid(column=1,row=1)
        
        #Username to delete
        self.deleteUsernameLabel = Label(self.root,
                                         text='Username to Delete',)
        self.deleteUsernameLabel.grid(column=0,row=2,columnspan=2)
        self.deleteUsernameEntry = Entry(self.root,
                                         textvariable=self.deleteUsername,
                                         width = int(self.windowWidth/7.1),
                                         border=3)
        self.deleteUsernameEntry.grid(column=0,row=3,columnspan=2)
        
        self.deleteUserBut = Button(self.root,
                                    text='Delete User',
                                    command=self.deleteUser,
                                    width=int(self.windowWidth/7.1))
        self.deleteUserBut.grid(column=0,row=4,columnspan=2)
        
        self.backBut = Button(self.root,
                              text='Back',
                              command = self.back,
                              width=int(self.windowWidth/7.1))
        
        self.backBut.grid(column=0,row=5,columnspan=2)
    
    def deleteUser(self):
        checkLoginInfo = dbfunctions.checkPassword(self.username.get(),self.password.get())
        checkUserExists = dbfunctions.checkUserExists(self.deleteUsername.get())
        if checkLoginInfo and checkUserExists:
            self.root.destroy()
            confirmWin = confirmWindow(self.deleteUsername.get())
            
        if not checkLoginInfo:
            utilities.errorBox('Incorrect login info')
            
        if not checkUserExists:
            utilities.errorBox('User Does Not exist')
        
    def back(self):
        self.root.destroy()
        
class confirmWindow(): #Do not need to put in menu stack as it is conditional
    def __init__(self,username):
        self.username = username
        
        confirmation = messagebox.askquestion("askquestion", "Are you sure?")
        if confirmation == 'yes':
            self.confirm()
        
    def confirm(self):
        deleted = dbfunctions.deleteUser(self.username)
        if deleted:
            messagebox.showinfo('showinfo','User Deleted')

class tableWindow(agentConfigDimensions):
    def __init__(self,root,tables,menuStack):
        self.menuStack = menuStack
        tempArr = []
        tempArr.append('tableWindow')
        tempArr.append(root)
        tempArr.append(tables)
        self.menuStack.push(tempArr)
        
        self.root = root
        self.tableLabel = Label(self.root,
                                text='Select Which Table to View')
        tempArr=[]
        self.tableLabel.pack()
        for table in tables:
            tempBut = Button(self.root,
                             text=table)
            tempArr.append(tempBut)
            
        for i in range(len(tempArr)):
            tempArr[i].config(command=partial(self.displaytable,tempArr[i].cget('text')))
            tempArr[i].pack()
            
    def displaytable(self,tableName):
        results = dbfunctions.retrieveTable(tableName)
        root2 = Toplevel(self.root)
        tableWin = dataDisplay(root2,results,tableName ,self.menuStack)

class dataDisplay():
    def __init__(self,root,results,tableName,menuStack):
        self.menuStack = menuStack
        tempArr = []
        tempArr.append('dataDisplay')
        tempArr.append(root)
        tempArr.append(results)
        tempArr.append(tableName)
        self.menuStack.push(tempArr)
        self.root = root
        
        
        
        self.results = results
        self.columnNames = dbfunctions.retrieveColumnNames(tableName)
        
        for i in range(len(self.columnNames)):
            if self.columnNames[i]!=None:
                tempLabel = Label(self.root,
                                  text=self.columnNames[i],
                                  fg='red')
                tempLabel.grid(column=i,row=0)
                    
        for y in range(len(self.results)):
            for x in range(len(self.results[y])):
                tempLabel = Label(self.root,
                                  text=self.results[y][x])
                tempLabel.grid(column=x,row=y+1)
class utilities():
    def backFunc(menuStack):
        menuStack.pop()

        if not menuStack.is_empty():
            win2Load = menuStack.peak()
            class2call = win2Load[0]
            class2call = class2call.lower()
            
            if class2call == 'loginpage':
                loginPage(menuStack)
                
            elif class2call =='postloginoptions':
                postLoginoptions(win2Load[1],win2Load[2],win2Load[3],win2Load[4],menuStack,True)

            elif class2call == 'admincontrolwindow':
                adminControlWindow(menuStack,True)
                
            elif class2call == 'loadsimwindow':
                loadSimWindow(win2Load[1],win2Load[2],menuStack)
            
            elif class2call == 'agentconfig':
                agentConfig(win2Load[1],win2Load[2],win2Load[3],win2Load[4],win2Load[5],menuStack)
                
            elif class2call == 'tablewindow':
                tableWindow(win2Load[1],win2Load[2],menuStack)
                
            elif class2call == 'datadisplay':
                dataDisplay(win2Load[1],win2Load[2],win2Load[3],menuStack)
        else:
            access()
        
    def errorBox(message):
        messagebox.showerror('Error',message)
        